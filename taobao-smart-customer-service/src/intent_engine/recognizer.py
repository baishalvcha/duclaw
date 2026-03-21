#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
意图识别引擎
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta


class IntentRecognizer:
    """意图识别器基类"""
    
    def __init__(self):
        """初始化意图识别器"""
        self.intent_keywords = {
            "pre_sale": ["价格", "多少钱", "功能", "怎么买", "购买", "优惠", "版本"],
            "in_sale": ["订单", "发货", "物流", "快递", "运单号", "收货", "付款"],
            "after_sale": ["安装", "配置", "问题", "错误", "bug", "教程", "售后"]
        }
    
    async def recognize(self, message_content):
        """识别消息意图"""
        content_lower = message_content.lower()
        
        # 统计关键词出现次数
        intent_scores = {}
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for kw in keywords if kw in content_lower)
            if score > 0:
                intent_scores[intent] = score
        
        # 返回最高分的意图
        if intent_scores:
            return max(intent_scores.items(), key=lambda x: x[1])[0]
        return "unknown"


class IntentContextManager:
    """意图上下文管理器"""
    
    def __init__(self):
        """初始化意图上下文管理器"""
        self.user_contexts = {}  # 用户ID -> 意图历史
    
    def update_context(self, user_id, intent, message):
        """更新用户意图上下文"""
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = []
        self.user_contexts[user_id].append({
            "timestamp": datetime.now(),
            "intent": intent,
            "message": message
        })
    
    def get_recent_intent(self, user_id, lookback_minutes=30):
        """获取最近意图"""
        if user_id not in self.user_contexts:
            return None
        
        # 过滤出最近一段时间内的意图
        cutoff_time = datetime.now() - timedelta(minutes=lookback_minutes)
        recent_contexts = [
            ctx for ctx in self.user_contexts[user_id]
            if ctx["timestamp"] >= cutoff_time
        ]
        
        if not recent_contexts:
            return None
        
        # 统计最近意图的出现次数
        intent_counts = {}
        for ctx in recent_contexts:
            intent = ctx["intent"]
            if intent != "unknown":
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        # 返回出现次数最多的意图
        if intent_counts:
            return max(intent_counts.items(), key=lambda x: x[1])[0]
        return None
