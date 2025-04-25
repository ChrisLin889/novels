"""
敏感词自动扫描调度器启动脚本
该脚本可以单独运行，也可以通过运维脚本调用

使用方法：
python backend/scripts/setup_scheduler.py
"""

import sys
import os
import logging

# 将项目根目录添加到PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask import Flask
from backend.app import create_app
from backend.app.utils.scheduler import start_scheduler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('scheduler.log')
    ]
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("启动敏感词扫描调度器...")
    
    try:
        app = create_app()
        with app.app_context():
            start_scheduler()
            logger.info("调度器启动成功，将在后台运行")
            
            # 保持脚本运行
            import time
            while True:
                time.sleep(60)
                
    except Exception as e:
        logger.error(f"调度器启动失败: {str(e)}")
        sys.exit(1) 