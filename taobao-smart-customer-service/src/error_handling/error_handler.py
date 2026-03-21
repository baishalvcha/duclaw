#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误处理器
"""

import logging
from typing import Dict, Any, Optional


class ErrorHandler:
    """错误处理器"""
    
    def __init__(self):
        """初始化错误处理器"""
        self.fallback_responses = {
            "taobao_api_error": "淘宝接口暂时不可用，请稍后重试或联系客服。",
            "intent_recognize_error": "正在理解您的问题，请稍等...",
            "role_handler_error": "系统正在升级，请描述您的问题，我会尽力帮您解决。",
            "knowledge_base_error": "知识库正在更新，请直接描述问题。"
        }
    
    async def handle_error(self, error_type: str, original_message: str, context: Dict[str, Any]) -> str:
        """处理错误并返回降级响应"""
        # 获取降级响应
        fallback_response = self.fallback_responses.get(
            error_type,
            "系统暂时遇到问题，请稍后重试。"
        )
        
        # 记录错误日志
        logging.error(f"Error type: {error_type}, Message: {original_message}")
        
        # 添加Judy人设化降级响应
        if error_type in ["taobao_api_error", "role_handler_error"]:
            return f"我是Judy，OpenClaw技术专家。{fallback_response}"
        else:
            return fallback_response
