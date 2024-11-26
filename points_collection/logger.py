import sys

from loguru import logger

# 配置日志记录器
logger.remove()  # 删除所有现有的日志处理程序
logger.add(sink=sys.stderr, level="INFO")
logger.add("./user_data/logs/points_collection.log", level="INFO", rotation="12:00")
logger.add("./user_data/logs/error.log", backtrace=False, diagnose=False, level="ERROR")
