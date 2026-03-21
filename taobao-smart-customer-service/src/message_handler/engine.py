#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息处理引擎
"""

from typing import Dict, Any, Optional, List
from src.intent_engine.engine import IntentEngine
from src.role_dispatcher.dispatcher import RoleDispatcher


class MessageHandler:
    """消息处理引擎"""
    
    def __init__(self):
        """初始化消息处理引擎"""
        self.intent_engine = IntentEngine()
        self.role_dispatcher = RoleDispatcher()
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """处理消息"""
        # 1. 提取消息内容
        user_id = message.get("user_id")
        content = message.get("content")
        message_type = message.get("type", "text")
        
        # 2. 识别意图
        intent = self.intent_engine.recognize_intent(content)
        
        # 3. 分配角色
        role = self.role_dispatcher.dispatch_role(intent, message)
        
        # 4. 生成响应
        response = self.generate_response(role, content, intent, message)
        
        return {
            "user_id": user_id,
            "intent": intent,
            "role": role,
            "response": response,
            "timestamp": message.get("timestamp")
        }
    
    def generate_response(self, role: str, content: str, intent: Dict[str, Any], 
                         message: Dict[str, Any]) -> str:
        """生成响应"""
        # 根据不同角色生成不同的响应
        # 实际应用中需要调用相应的角色处理器
        if role == "judy":
            return f"【Judy】正在处理您的问题: {content}"
        elif role == "bee":
            return f"【Bee】已收到您的消息: {content}"
        elif role == "order_bot":
            return f"【OrderBot】正在查询您的订单信息"
        else:
            return f"正在处理您的消息: {content}"
    
    def batch_process_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量处理消息"""
        results = []
        for message in messages:
            result = self.process_message(message)
            results.append(result)
        return results
