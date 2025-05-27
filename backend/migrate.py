#!/usr/bin/env python
"""
数据库迁移脚本
用法: python migrate.py
"""
import sys
import time
from app.utils.db_migration import run_migration
from app.core.logging import logger

if __name__ == "__main__":
    try:
        logger.info("开始数据迁移...")
        start_time = time.time()
        
        # 执行数据迁移
        run_migration()
        
        elapsed = time.time() - start_time
        logger.info(f"数据迁移完成，耗时 {elapsed:.2f} 秒")
    except Exception as e:
        logger.error(f"数据迁移失败: {e}")
        sys.exit(1)
    
    sys.exit(0) 