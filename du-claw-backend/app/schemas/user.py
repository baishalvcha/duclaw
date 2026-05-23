"""Pydantic Schemas — 用户相关。"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    """微信登录请求体。"""
    code: str


class UserResponse(BaseModel):
    """用户信息响应。"""
    id: UUID
    openid: str
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class LoginResponse(BaseModel):
    """登录成功响应（含 JWT token）。"""
    user: UserResponse
    token: str


class RemainCountResponse(BaseModel):
    """各场景剩余次数。"""
    scene_type: str
    remain_count: int
    total_used: int

    model_config = {"from_attributes": True}