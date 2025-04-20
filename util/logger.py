import logging
from pathlib import Path
from datetime import datetime
from config.settings import Settings as settings  # 导入配置模块

def setup_logger(name):
    """配置并返回一个日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 如果已经配置过处理器则不再重复配置
    if logger.handlers:
        return logger
    
    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    log_file = Path(settings.PATH) / f"logs/{datetime.now().strftime('%Y%m%d')}.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)  # 创建目录
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
