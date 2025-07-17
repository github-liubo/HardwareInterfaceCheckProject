# logger_config.py
import logging
import sys

class StdoutLogger:
    """将 stdout 的 print 内容转为 logging.info"""
    def __init__(self, level=logging.INFO):
        self.level = level

    def write(self, buffer):
        buffer = buffer.strip()
        if buffer:
            logging.log(self.level, buffer)

    def flush(self):
        pass  # 忽略 flush 方法


def setup_logger(log_file='monitor.log'):
    # 配置基础日志格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # 可选：继续输出到控制台
        ]
    )

    # 重定向 stdout
    sys.stdout = StdoutLogger(logging.INFO)

    logging.info("日志系统已初始化")
    # logger_config.py
    ...

