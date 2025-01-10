# log_config.py
import sys
from datetime import datetime

import loguru

# 创建并配置 logger 对象
logger = loguru.logger


def setup_logger(debug=False):
    """
    设置日志记录器，输出日志到控制台和文件。

    参数:
        debug (bool): 如果为 True，日志级别为 DEBUG，否则为 INFO。
    """
    logger.remove()  # 移除默认的日志处理器

    # 设置日志级别
    log_level = "DEBUG" if debug else "INFO"

    # 控制台输出，启用颜色
    # 获取当前控制台宽度
    import shutil
    console_width = shutil.get_terminal_size().columns

    # 自定义换行函数
    def wrap_text(text, width):
        """使用 textwrap 对文本进行换行"""
        import textwrap
        return "\n".join(textwrap.wrap(text, width=width))

    # 定义一个处理每条日志消息的函数，自动换行
    def log_message_with_wrap(record):
        """对日志消息进行自动换行处理"""
        # 获取日志消息
        message = record["message"]
        # 根据控制台宽度的60%来计算换行宽度
        wrapped_message = wrap_text(message, int(console_width * 0.6))
        # 将处理后的消息返回
        record["message"] = wrapped_message
        return record

    # 配置 logger
    logger.add(
        sys.stdout,
        level=log_level,
        colorize=True,  # 启用颜色输出
        backtrace=True,
        diagnose=True,
        enqueue=True,  # 启用多线程支持
        # filter=log_message_with_wrap  # 使用自定义过滤器进行消息处理
    )

    # 设置文件日志处理器（普通日志文件）
    date = datetime.now().strftime('%Y-%m-%d')
    logger.add(
        f"logs\\nagi_{date}.log",
        level=log_level,
        rotation="3 MB",  # 轮转条件
        compression="zip",  # 轮转时压缩日志文件
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",  # 文件日志格式
        backtrace=True,  # 记录回溯信息
        diagnose=True,  # 捕捉异常详细信息
    )

    # 设置错误日志文件（只记录 ERROR 和 CRITICAL）
    logger.add(
        f"logs\\nagi_error_{date}.log",
        level="ERROR",  # 只记录 ERROR 及以上级别日志
        rotation="3 MB",  # 轮转条件
        compression="zip",  # 轮转时压缩日志文件
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",  # 错误日志文件格式
        backtrace=True,  # 记录回溯信息
        diagnose=True,  # 捕捉异常详细信息
    )


# 调用 setup_logger 配置日志
setup_logger(debug=False)
# setup_logger(debug=True)
