from loguru import logger
import sys
import inspect

class CustomLogger:
    def __init__(self):
        # 创建一个自定义的 logger 实例
        self.custom_logger = logger

        # 添加自定义属性
        self.custom_logger.level_mapping = {
            "DEBUG": 10,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50,
            "TRACE": 5,
            "SUCCESS": 25,
            "INFO": 20,
        }
        self.custom_logger.default_level = 20
        self.custom_logger.reverse_level_mapping = {v: k for k, v in self.custom_logger.level_mapping.items()}

        def _get_level_name(level):
            """
            获取数字级别对应的文本级别名称。
            """
            if isinstance(level, str):
                level = level.upper()
                if level in self.custom_logger.level_mapping:
                    level = self.custom_logger.level_mapping[level]
                else:
                    level = self.custom_logger.default_level
            return self.custom_logger.reverse_level_mapping.get(level, "UNKNOWN")

        def custom_format(record):
            """
            自定义的 format 函数，将数字级别的名称替换为文本形式的级别名称。
            """
            level_name = _get_level_name(record["level"].no)
            record["level"].name = level_name
            frame = inspect.currentframe().f_back.f_back
            return "{time:YYYY-MM-DD HH:mm:ss.SSS} | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>\n".format(
                time=record["time"],
                level=record["level"].name,
                name=frame.f_code.co_filename,
                function=frame.f_code.co_name,
                line=frame.f_lineno,
                message=record["message"]
            )

        # 配置 logger
        self.custom_logger.add(
            sys.stdout,
            level=0,
            colorize=True,  # 启用颜色输出
            backtrace=True,
            diagnose=True,
            enqueue=True,  # 启用多线程支持
            format=custom_format
        )

    def add_level(self, name, level, color=None, icon=None):
        """
        添加自定义级别，并将其映射到数字级别。
        """
        if name.upper() in self.custom_logger.level_mapping:
            raise ValueError(f"Level '{name}' is already defined in level_mapping.")

        self.custom_logger.level_mapping[name.upper()] = level
        self.custom_logger.reverse_level_mapping = {v: k for k, v in self.custom_logger.level_mapping.items()} # 添加反向映射

    def log(self, level, message, *args, **kwargs):
        """
        使用自定义的级别映射记录日志。
        """
        if isinstance(level, str):
            level = level.upper()
            if level in self.custom_logger.level_mapping:
                level = self.custom_logger.level_mapping[level]
            else:
                level = self.custom_logger.default_level  # 如果未找到，则使用默认级别
        self.custom_logger.log(level, message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        self.custom_logger.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self.custom_logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.custom_logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self.custom_logger.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        self.custom_logger.critical(message, *args, **kwargs)

    def trace(self, message, *args, **kwargs):
        self.custom_logger.trace(message, *args, **kwargs)

    def success(self, message, *args, **kwargs):
        self.custom_logger.success(message, *args, **kwargs)

logger = CustomLogger()
if __name__ == "__main__":
    logger.add_level("卧槽", 999)
    logger.log("卧槽", "卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧槽卧")
    logger.log(9999,"qqqq")
