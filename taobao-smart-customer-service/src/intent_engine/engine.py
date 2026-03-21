#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
意图识别引擎
"""

from typing import Dict, Any, List
import re


class IntentEngine:
    """意图识别引擎"""
    
    def __init__(self):
        """初始化意图识别引擎"""
        self.intent_patterns = {
            "order_status": [
                r"订单.*状态",
                r"我的订单",
                r"订单.*查询",
                r"订单.*什么时候到",
                r"物流.*信息"
            ],
            "product_info": [
                r"商品.*信息",
                r"产品.*详情",
                r"商品.*规格",
                r"商品.*价格",
                r"商品.*库存"
            ],
            "refund": [
                r"退款",
                r"退货",
                r"退款.*流程",
                r"退货.*流程",
                r"退款.*申请"
            ],
            "complaint": [
                r"投诉",
                r"不满",
                r"问题",
                r"质量",
                r"服务.*差"
            ],
            "general_question": [
                r"你好",
                r"在吗",
                r"请问",
                r"帮助",
                r"支持"
            ]
        }
    
    def recognize_intent(self, message: str) -> Dict[str, Any]:
        """识别消息意图"""
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message):
                    return {
                        "intent": intent,
                        "confidence": 0.9,
                        "keywords": self.extract_keywords(message)
                    }
        
        # 默认意图
        return {
            "intent": "general_question",
            "confidence": 0.5,
            "keywords": self.extract_keywords(message)
        }
    
    def extract_keywords(self, message: str) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取
        # 实际应用中可以使用更复杂的NLP技术
        keywords = []
        
        # 提取订单号
        order_pattern = r"订单号[:：]?\s*([0-9]+)"
        order_match = re.search(order_pattern, message)
        if order_match:
            keywords.append(f"订单号:{order_match.group(1)}")
        
        # 提取商品相关关键词
        product_patterns = [r"商品[:：]?\s*([^，,。.]+)", r"产品[:：]?\s*([^，,。.]+)"]
        for pattern in product_patterns:
            match = re.search(pattern, message)
            if match:
                keywords.append(f"商品:{match.group(1)}")
        
        return keywords
    
    def batch_recognize_intent(self, messages: List[str]) -> List[Dict[str, Any]]:
        """批量识别意图"""
        results = []
        for message in messages:
            result = self.recognize_intent(message)
            results.append(result)
        return results
