#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息处理模块
"""

from .pipeline import MessageProcessingPipeline, MessageLogger, MessageValidator
from .engine import MessageHandler


class Message:
    """消息类"""
    
    def __init__(self, content: str, user_id: str = "", msg_type: str = "text"):
        """初始化消息"""
        self.content = content
        self.user_id = user_id
        self.msg_type = msg_type
        self.timestamp = None
    
    def __str__(self):
        """字符串表示"""
        return f"Message(content='{self.content}', user_id='{self.user_id}', type='{self.msg_type}')"


__all__ = [
    "MessageProcessingPipeline",
    "MessageLogger",
    "MessageValidator",
    "MessageHandler",
    "Message"
]