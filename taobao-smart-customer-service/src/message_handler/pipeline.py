#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息处理管道
"""

import logging
from typing import List, Any, Optional


class MessageProcessingPipeline:
    """消息处理管道"""
    
    def __init__(self):
        """初始化消息处理管道"""
        self.processors = []
    
    def add_processor(self, processor):
        """添加消息处理器"""
        self.processors.append(processor)
    
    async def process(self, message):
        """处理消息"""
        result = message
        for processor in self.processors:
            result = await processor.process(result)
        return result


class MessageLogger:
    """消息日志记录器"""
    
    async def process(self, message):
        """记录消息日志"""
        logging.info(f"收到消息: {message}")
        return message


class MessageValidator:
    """消息验证器"""
    
    async def process(self, message):
        """验证消息有效性"""
        if not hasattr(message, 'content') or not message.content or len(message.content.strip()) == 0:
            raise ValueError("消息内容为空")
        return message
