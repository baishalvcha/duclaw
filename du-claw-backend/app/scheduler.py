"""定时任务调度器 —— 使用 APScheduler 的 AsyncIOScheduler 每分钟扫描日程提醒。"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

from app.database import async_session_factory
from app.services.schedule_service import ScheduleService

scheduler = AsyncIOScheduler()


async def scan_and_notify_job():
    """每分钟执行的定时任务：扫描待提醒日程并推送。"""
    logger.info("Running scheduled scan for reminders...")
    try:
        async with async_session_factory() as session:
            svc = ScheduleService(session)
            await svc.scan_and_notify(async_session_factory)
    except Exception as e:
        logger.error(f"Scheduled job failed: {e}")


def start_scheduler():
    """启动定时任务调度器。"""
    trigger = IntervalTrigger(minutes=1)
    scheduler.add_job(
        scan_and_notify_job,
        trigger=trigger,
        id="scan_reminders",
        name="每分钟扫描日程提醒",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started: scan reminders every minute")


def stop_scheduler():
    """停止定时任务调度器。"""
    scheduler.shutdown()
    logger.info("Scheduler stopped")