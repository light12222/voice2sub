"""🎛️ Central configuration for BilinBubble."""

from pathlib import Path

# ───── Whisper 模型设置 ─────
MODEL_SIZE: str = "medium.en"    # 推荐使用 medium.en 或 large-v2
USE_WHISPERX: bool = True        # 当前项目使用 WhisperX 后端

# ───── 目标翻译语言 ─────
TARGET_LANG: str = "zh-cn"       # 用于 Google Translate，可改为 "en", "ja", etc.

# ───── 音频参数设置 ─────
AUDIO_RATE: int = 16_000         # 采样率：16kHz
CHUNK_SIZE: int = 4_000          # 每帧样本数：0.25 秒
MIN_AUDIO_SEC: float = 0.5       # 最小音频时长（秒）：小于此值不触发识别

# ───── 日志输出位置 ─────
LOG_PATH: Path = Path("output/log.txt")  # 自动创建路径

# ───── 字幕窗口设置 ─────
FONT_SIZE: int = 20              # 字体大小（pt）
WINDOW_OPACITY: float = 0.85     # 窗口透明度：0=全透明，1=不透明
