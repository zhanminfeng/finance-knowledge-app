import logging
import sys
from app.core.config import settings

def setup_logging() -> logging.Logger:
    """配置应用日志"""
    
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    # 配置根日志器
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    # 设置第三方库的日志级别
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    # 创建应用日志器
    logger = logging.getLogger("app")
    logger.setLevel(log_level)
    
    return logger

# 创建日志器单例
logger = setup_logging() 