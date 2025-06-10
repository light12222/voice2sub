import sys
from pathlib import Path
from datetime import datetime
from loguru import logger

# ✅ 初始化 loguru 日志记录器
def setup_logger(log_path: Path):
    logger.remove()  # 移除默认的 stderr 输出
    logger.add(log_path, encoding="utf-8", enqueue=True, backtrace=True, diagnose=True)
    logger.add(sys.stderr, level="DEBUG")  # 控制台调试用

# ✅ 文本转写 + 翻译日志记录器
class LogWriter:
    def __init__(self, log_file: Path = Path("output/log.txt")):
        log_file.parent.mkdir(parents=True, exist_ok=True)
        self.log_file = log_file.open("a", encoding="utf-8")

    def write(self, source: str, translated: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}]\n原文: {source}\n翻译: {translated}\n\n"
        self.log_file.write(entry)
        self.log_file.flush()
