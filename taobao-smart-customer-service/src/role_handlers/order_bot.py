#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OrderBot角色处理器
"""

from typing import Dict, Any, Optional
import re


class OrderBotHandler:
    """OrderBot角色处理器 - 处理订单相关问题"""
    
    def __init__(self):
        """初始化OrderBot处理器"""
        pass
    
    def handle_message(self, message: Dict[str, Any], intent: Dict[str, Any]) -> str:
        """处理消息"""
        content = message.get("content", "")
        intent_type = intent.get("intent", "general_question")
        
        if intent_type == "order_status":
            order_id = self._extract_order_id(content)
            if order_id:
                return self._handle_order_status(order_id)
            else:
                return self._request_order_id()
        else:
            return self._handle_general(content)
    
    def _extract_order_id(self, content: str) -> Optional[str]:
        """提取订单号"""
        order_pattern = r"订单号[:：]?\s*([0-9]+)"
        match = re.search(order_pattern, content)
        if match:
            return match.group(1)
        return None
    
    def _handle_order_status(self, order_id: str) -> str:
        """处理订单状态查询"""
        return f"【OrderBot】正在查询您的订单 {order_id} 的状态，请稍候..."
    
    def _request_order_id(self) -> str:
        """请求订单号"""
        return "【OrderBot】您好，为了查询您的订单状态，请提供您的订单号。"
    
    def _handle_general(self, content: str) -> str:
        """处理一般问题"""
        return "【OrderBot】您好，我是订单助手，有什么可以帮助您的吗？"
