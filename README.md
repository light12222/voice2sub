---

````markdown
# Voice2Sub

Real-time speech-to-subtitle and translation overlay for your screen, built with WhisperX and PyQt5.

---

## What is Voice2Sub?

Voice2Sub is a lightweight desktop tool that listens to your voice, transcribes it using WhisperX, translates it into your target language (like Chinese), and displays **bilingual subtitles** as an overlay on your screen — in real time.

It works fully offline (for transcription) and requires no API key for translation (via Google Translate).

---

## Features

- 🎙️ Real-time microphone transcription (WhisperX)
- 🌐 Bilingual translation overlay (e.g. English → 中文)
- 🪟 Frameless always-on-top subtitle window (PyQt5)
- 🔇 Noise filtering + text de-duplication
- 📜 Auto logging of raw and translated text
- ⚙️ Customizable language, font, opacity, model size

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/light12222/voice2sub.git
cd voice2sub
````

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

```bash
python main_debug.py
```

> A floating subtitle box will appear. Speak into your microphone, and see live translation.

---

## Configuration

You can edit `config.py` to change:

```python
MODEL_SIZE = "medium.en"     # WhisperX model
TARGET_LANG = "zh-cn"        # Translation language
FONT_SIZE = 20               # Subtitle font size
WINDOW_OPACITY = 0.85        # 0 = transparent, 1 = solid
```

---

## Tech Stack

* [WhisperX](https://github.com/m-bain/whisperx) for ASR
* [googletrans](https://pypi.org/project/googletrans/) for translation
* [PyQt5](https://pypi.org/project/PyQt5/) for the UI
* [PyAudio](https://pypi.org/project/PyAudio/) for mic input
* [loguru](https://github.com/Delgan/loguru) for logging

---

## Roadmap

* [x] Real-time ASR + translation
* [x] Frameless PyQt5 overlay
* [ ] OBS plugin / livestream support
* [ ] Offline translation (Argos)
* [ ] Voice activity segmentation (VAD)

---

## License

MIT License © 2025 Yin Wang

---

## Credits

* OpenAI Whisper / WhisperX
* Silero VAD (planned)
* PyQt5, googletrans, loguru

````

---
