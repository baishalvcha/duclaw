#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API请求/响应模型
"""

from pydantic import BaseModel
from typing import Optional


class TaobaoWebhookRequest(BaseModel):
    """淘宝Webhook请求模型"""
    app_key: str
    timestamp: str
    sign: str
    msg_id: str
    buyer_id: str
    content: str
    msg_type: str = "text"


class ProcessingResponse(BaseModel):
    """处理响应模型"""
    success: bool
    intent: Optional[str] = None
    role: Optional[str] = None
    response_content: Optional[str] = None
    error_message: Optional[str] = None
