"""Pydantic Schemas — 日程提醒。"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ScheduleCreate(BaseModel):
    """创建日程。"""
    title: str
    description: Optional[str] = None
    remind_time: datetime


class ScheduleResponse(BaseModel):
    """日程响应。"""
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    remind_time: datetime
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ScheduleUpdate(BaseModel):
    """更新日程（部分字段）。"""
    title: Optional[str] = None
    description: Optional[str] = None
    remind_time: Optional[datetime] = None
    is_completed: Optional[bool] = None