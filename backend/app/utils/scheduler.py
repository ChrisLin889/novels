import schedule
import time
import threading
from app.utils.tasks import scan_and_update_content
import logging

logger = logging.getLogger(__name__)

def run_scheduler():
    """运行定时任务调度器"""
    # 每天凌晨3点执行敏感词自动扫描
    schedule.every().day.at("03:00").do(scan_and_update_content)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次

def start_scheduler():
    """启动调度器线程"""
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    logger.info("敏感词自动扫描调度器已启动") 