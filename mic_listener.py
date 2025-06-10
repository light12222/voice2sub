# mic_listener.py (WhisperX version with float32)
# ✅ WhisperX + Resample + 去重 + 多段识别 + 超时保护 + PyAudio 封装

import queue
import threading
import numpy as np
import resampy
import pyaudio
import concurrent.futures
from loguru import logger
import torch
import whisperx  # ✅ WhisperX 替代 faster-whisper

AUDIO_RATE = 16000  # Whisper expects 16kHz
CHUNK = 4000
MIN_AUDIO_LEN = int(AUDIO_RATE * 3.5)  # ✅ 提高缓冲下限至 3.5 秒，确保完整句子
MAX_BUFFER_SECONDS = 6
MIN_VOLUME = 0.005

class TranscriptDeduplicator:
    def __init__(self):
        self.last_text = ""
        self.history = set()

    def is_duplicate(self, text: str) -> bool:
        text = text.strip()
        if not text:
            return True
        if text == self.last_text or text in self.history:
            return True
        self.last_text = text
        self.history.add(text)
        return False

def transcribe_with_timeout(model, audio, timeout=10):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(model.transcribe, audio, batch_size=16)
        return future.result(timeout=timeout)

class MicTranscriberVAD:
    def __init__(self, model_size="medium.en", on_text=None):
        self.audio_queue = queue.Queue()
        self.running = False
        self.audio_buffer = []
        self.on_text = on_text

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisperx.load_model(model_size, self.device, compute_type="float32")
        self.deduplicator = TranscriptDeduplicator()
        self.audio_interface = None
        self.input_rate = 48000

    def _callback(self, in_data, frame_count, time_info, status):
        audio_np = np.frombuffer(in_data, dtype=np.int16).astype(np.float32) / 32768.0
        if self.input_rate != AUDIO_RATE:
            audio_np = resampy.resample(audio_np, self.input_rate, AUDIO_RATE)
        self.audio_queue.put(audio_np)
        return (in_data, pyaudio.paContinue)

    def _processing_loop(self):
        logger.info("🎙️ WhisperX processing thread started.")
        max_samples = AUDIO_RATE * MAX_BUFFER_SECONDS

        while self.running:
            try:
                audio_chunk = self.audio_queue.get(timeout=1)
            except queue.Empty:
                continue

            rms = np.sqrt(np.mean(audio_chunk ** 2))
            logger.debug(f"🔊 RMS Volume: {rms:.5f}")
            if rms < MIN_VOLUME:
                continue

            self.audio_buffer.append(audio_chunk)
            full_audio = np.concatenate(self.audio_buffer, axis=0)
            logger.debug(f"🧠 Audio buffer size: {len(full_audio)} samples")

            if len(full_audio) < MIN_AUDIO_LEN:
                continue

            if len(full_audio) > max_samples:
                logger.warning("🧹 缓冲区超过最大限制，强制识别")

            try:
                logger.info("🔍 Transcribing via WhisperX...")
                result = transcribe_with_timeout(self.model, full_audio, timeout=10)
                segments = result.get("segments", [])
                for segment in segments:
                    text = segment["text"].strip()
                    # ✅ 放宽短文本过滤门槛，仅跳过少于2词的
                    if len(text.split()) < 2:
                        logger.debug("⏭️ 识别文本过短，跳过")
                        continue
                    if self.deduplicator.is_duplicate(text):
                        logger.debug("⏭️ 重复或空文本跳过")
                        continue
                    logger.info(f"🗣️ WhisperX: {text}")
                    if self.on_text:
                        self.on_text(text)
            except concurrent.futures.TimeoutError:
                logger.warning("⏳ WhisperX 推理超时，跳过该段音频")
            except Exception as e:
                logger.exception(f"[WhisperX] Transcription error: {e}")

            self.audio_buffer = []

    def start(self):
        logger.info("📱 Starting MicTranscriber...")
        self.running = True
        self.audio_interface = pyaudio.PyAudio()
        try:
            dev_info = self.audio_interface.get_default_input_device_info()
            self.input_rate = int(dev_info["defaultSampleRate"])
            logger.info(f"🎸 Detected input rate: {self.input_rate} Hz")
        except Exception as e:
            logger.warning(f"⚠️ 获取默认采样率失败，使用默认 48kHz: {e}")

        self.stream = self.audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.input_rate,
            input=True,
            frames_per_buffer=CHUNK,
            stream_callback=self._callback
        )
        self.stream.start_stream()
        threading.Thread(target=self._processing_loop, daemon=True).start()

    def stop(self):
        self.running = False
        if hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()
        if self.audio_interface:
            self.audio_interface.terminate()
        logger.info("🛑 MicTranscriber stopped.")
