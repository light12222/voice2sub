from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from config import FONT_SIZE, WINDOW_OPACITY
from loguru import logger

class SubtitleWindow(QWidget):
    def __init__(self):
        # ✅ 使用普通窗口方便调试，避免隐藏在后台
        super().__init__(flags=Qt.Window | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(WINDOW_OPACITY)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # 🔤 英文原文
        self.label_en = QLabel("...")
        self.label_en.setAlignment(Qt.AlignCenter)
        self.label_en.setStyleSheet(f"color: white; font-size: {FONT_SIZE}pt; background-color: black; padding: 6px;")

        # 🈶 中文翻译
        self.label_zh = QLabel("...")
        self.label_zh.setAlignment(Qt.AlignCenter)
        self.label_zh.setStyleSheet(f"color: #80ff80; font-size: {FONT_SIZE - 2}pt; background-color: black; padding: 6px;")

        layout.addWidget(self.label_en)
        layout.addWidget(self.label_zh)
        self.setLayout(layout)

        self.resize(700, 120)
        self.move(100, 100)

        logger.info("🪟 SubtitleWindow 双语模式初始化完成 ✅")

    def set_text(self, text_en: str, text_zh: str = ""):
        logger.debug(f"[Subtitle] 英文: {text_en} ｜ 中文: {text_zh}")
        self.label_en.setText(text_en)
        self.label_zh.setText(text_zh)
