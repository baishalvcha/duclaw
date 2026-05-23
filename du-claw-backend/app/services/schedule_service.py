"""日程提醒服务 —— 创建、查询、完成、删除日程，以及定时扫描推送提醒。"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schedule import Schedule


class ScheduleService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_schedule(
        self, user_id: UUID, title: str, description: Optional[str], remind_time: datetime
    ) -> Schedule:
        schedule = Schedule(
            user_id=user_id,
            title=title,
            description=description,
            remind_time=remind_time,
        )
        self.session.add(schedule)
        await self.session.commit()
        await self.session.refresh(schedule)
        logger.info(f"Schedule created: {schedule.id} for user {user_id}")
        return schedule

    async def get_today_schedules(self, user_id: UUID) -> List[Schedule]:
        now = datetime.now(timezone.utc)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        stmt = (
            select(Schedule)
            .where(
                Schedule.user_id == user_id,
                Schedule.remind_time >= start_of_day,
                Schedule.remind_time <= end_of_day,
            )
            .order_by(Schedule.remind_time)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_all_schedules(self, user_id: UUID) -> List[Schedule]:
        stmt = (
            select(Schedule)
            .where(Schedule.user_id == user_id)
            .order_by(Schedule.remind_time)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def complete_schedule(
        self, schedule_id: UUID, user_id: UUID
    ) -> Optional[Schedule]:
        stmt = select(Schedule).where(
            Schedule.id == schedule_id, Schedule.user_id == user_id
        )
        result = await self.session.execute(stmt)
        schedule = result.scalar_one_or_none()
        if schedule is None:
            return None

        schedule.is_completed = True
        await self.session.commit()
        await self.session.refresh(schedule)
        logger.info(f"Schedule {schedule_id} marked as completed")
        return schedule

    async def delete_schedule(
        self, schedule_id: UUID, user_id: UUID
    ) -> bool:
        stmt = select(Schedule).where(
            Schedule.id == schedule_id, Schedule.user_id == user_id
        )
        result = await self.session.execute(stmt)
        schedule = result.scalar_one_or_none()
        if schedule is None:
            return False

        await self.session.delete(schedule)
        await self.session.commit()
        logger.info(f"Schedule {schedule_id} deleted")
        return True

    async def scan_and_notify(self, db_session_factory) -> None:
        """每分钟扫描待提醒日程并推送（由 APScheduler 调用）。"""
        now = datetime.now(timezone.utc)
        # 查找 remind_time 在当前一分钟窗口内的未完成日程
        stmt = select(Schedule).where(
            Schedule.is_completed == False,
            Schedule.remind_time >= now.replace(second=0, microsecond=0),
            Schedule.remind_time < now.replace(second=59, microsecond=999999),
        )
        result = await self.session.execute(stmt)
        schedules = list(result.scalars().all())

        for s in schedules:
            logger.info(
                f"Reminder triggered: {s.title} for user {s.user_id} at {s.remind_time}"
            )
            # TODO: 接入微信模板消息推送
            # await wechat_service.send_reminder(s.user_id, s.title, s.description)

        if schedules:
            await self.session.commit()
            logger.info(f"Scanned and notified {len(schedules)} schedules")