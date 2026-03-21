#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
角色分配器
"""

from typing import Dict, Any, Optional
from src.role_handlers.bee_sales import BeeSalesHandler
from src.role_handlers.order_assistant import OrderAssistantHandler
from src.role_handlers.judy_tech import JudyTechHandler


class RoleDispatcher:
    """角色分配器"""
    
    def __init__(self):
        """初始化角色分配器"""
        self.role_mapping = {
            "pre_sale": "bee",       # 售前 → Bee（销售助理）
            "in_sale": "order_bot",  # 售中 → 订单助手
            "after_sale": "judy",    # 售后 → Judy（技术专家）
            "unknown": "judy"        # 未知 → 默认Judy
        }
        self.role_handlers = self.initialize_handlers()
    
    def initialize_handlers(self):
        """初始化角色处理器"""
        return {
            "bee": BeeSalesHandler(),
            "order_bot": OrderAssistantHandler(),
            "judy": JudyTechHandler()
        }
    
    async def dispatch(self, intent: str, message: Dict[str, Any], context: Dict[str, Any]) -> str:
        """分配角色并处理消息"""
        role = self.role_mapping.get(intent, "judy")
        handler = self.role_handlers.get(role)
        
        if handler:
            return await handler.handle(message, context)
        else:
            return "系统正在升级，请稍后重试。"
    
    def dispatch_role(self, intent: Dict[str, Any], message: Dict[str, Any]) -> str:
        """分配角色（兼容旧接口）"""
        # 从intent字典中提取意图类型
        intent_type = intent.get("intent", "unknown")
        # 映射到新的意图类型
        intent_mapping = {
            "order_status": "in_sale",
            "product_info": "pre_sale",
            "refund": "after_sale",
            "complaint": "after_sale",
            "general_question": "pre_sale"
        }
        new_intent_type = intent_mapping.get(intent_type, intent_type)
        # 返回角色
        return self.role_mapping.get(new_intent_type, "judy")
    
    def get_available_roles(self) -> list:
        """获取可用角色列表"""
        return list(set(self.role_mapping.values()))
    
    def update_role_mapping(self, intent_type: str, role: str):
        """更新角色映射"""
        self.role_mapping[intent_type] = role
