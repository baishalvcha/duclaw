"""Pydantic Schemas — 对话与消息。"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class ConversationCreate(BaseModel):
    """创建对话。"""
    scene_type: str
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    """对话响应。"""
    id: UUID
    user_id: UUID
    scene_type: str
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    model_config = {"from_attributes": True}


class MessageCreate(BaseModel):
    """创建消息。"""
    content: str


class MessageResponse(BaseModel):
    """消息响应。"""
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    token_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatRequest(BaseModel):
    """AI 对话请求。"""
    scene_type: str
    conversation_id: Optional[UUID] = None
    message: str


class ChatResponse(BaseModel):
    """AI 对话响应。"""
    reply: str
    conversation_id: UUID
    token_used: int