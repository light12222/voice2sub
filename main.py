import sys
from PyQt5.QtWidgets import QApplication
from subtitle_window import SubtitleWindow
from translator import TextTranslator
from log_writer import LogWriter
from mic_listener import MicTranscriberVAD
from loguru import logger
from config import MODEL_SIZE  # ✅ 可通过 config.py 控制模型大小

# ---------- 初始化 ----------
app = QApplication(sys.argv)
subtitle_window = SubtitleWindow()
subtitle_window.show()
subtitle_window.set_text("👃 Listening...", "正在监听中…")

translator = TextTranslator(dest_lang="zh-cn")
log_writer = LogWriter()

# ---------- 文本处理逻辑 ----------
def handle_text(text: str):
    text = text.strip()
    if not text:
        return
    logger.info(f"📋 Whisper: {text}")
    try:
        translated = translator.translate(text) or "(翻译失败)"
    except Exception as e:
        logger.warning(f"🌐 翻译失败: {e}")
        translated = "(翻译失败)"

    logger.info(f"🌐 Translated: {translated}")
    subtitle_window.set_text(text, translated)
    log_writer.write(text, translated)

# ---------- 麦克风监听器 ----------
listener = MicTranscriberVAD(model_size=MODEL_SIZE, on_text=handle_text)
listener.start()

# ---------- 主线程保持运行 ----------
try:
    sys.exit(app.exec_())
except KeyboardInterrupt:
    logger.info("⛘️ 捕获 Ctrl+C，程序退出")
    listener.stop()
    sys.exit(0)