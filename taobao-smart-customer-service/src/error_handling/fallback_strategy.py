#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
降级策略管理器
"""

from typing import Dict, Any, Optional
from src.role_handlers.judy_tech import JudyTechHandler


class FallbackStrategyManager:
    """降级策略管理器"""
    
    def __init__(self):
        """初始化降级策略管理器"""
        self.strategies = {
            "taobao_api_fallback": self.taobao_api_fallback,
            "intent_fallback": self.intent_fallback,
            "role_fallback": self.role_fallback
        }
    
    async def taobao_api_fallback(self, message: Dict[str, Any]) -> str:
        """淘宝API降级策略"""
        # 当淘宝API不可用时，使用本地缓存或简化回复
        return "淘宝服务暂时不可用，您可以：\n1. 稍后重试\n2. 加入QQ群获取帮助\n3. 联系客服微信"
    
    async def intent_fallback(self, message: Dict[str, Any]) -> str:
        """意图识别降级策略"""
        # 当意图识别失败时，使用通用回复
        return "请描述您的问题：\n• 价格/购买咨询\n• 订单/物流查询\n• 技术/售后问题"
    
    async def role_fallback(self, message: Dict[str, Any], intended_role: str) -> str:
        """角色处理器降级策略"""
        # 当角色处理器失败时，使用Judy作为默认
        judy_handler = JudyTechHandler()
        return await judy_handler.handle(message, {})
    
    async def apply_strategy(self, strategy_name: str, **kwargs) -> str:
        """应用降级策略"""
        strategy = self.strategies.get(strategy_name)
        if strategy:
            return await strategy(**kwargs)
        else:
            return "系统暂时遇到问题，请稍后重试。"
