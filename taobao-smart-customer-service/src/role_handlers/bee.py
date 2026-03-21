#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bee角色处理器
"""

from typing import Dict, Any, Optional


class BeeHandler:
    """Bee角色处理器 - 处理一般问题和商品信息查询"""
    
    def __init__(self):
        """初始化Bee处理器"""
        pass
    
    def handle_message(self, message: Dict[str, Any], intent: Dict[str, Any]) -> str:
        """处理消息"""
        content = message.get("content", "")
        intent_type = intent.get("intent", "general_question")
        
        if intent_type == "product_info":
            return self._handle_product_info(content)
        else:
            return self._handle_general(content)
    
    def _handle_product_info(self, content: str) -> str:
        """处理商品信息查询"""
        return "【Bee】您好，关于商品信息，我们需要了解更多细节。请提供商品名称或链接，我们会为您查询详细信息。"
    
    def _handle_general(self, content: str) -> str:
        """处理一般问题"""
        return "【Bee】您好，我是客服Bee，有什么可以帮助您的吗？"
