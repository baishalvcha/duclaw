#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
淘宝开放平台Webhook接收器
"""

from typing import Dict, Any, Optional
import hashlib


class TaobaoWebhookReceiver:
    """淘宝Webhook接收器"""
    
    def __init__(self, app_key: str, app_secret: str):
        """初始化Webhook接收器"""
        self.app_key = app_key
        self.app_secret = app_secret
    
    async def handle_webhook(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理淘宝Webhook回调"""
        try:
            # 1. 验证签名
            if not self.verify_signature(request_data):
                return {"error": "签名验证失败"}
            
            # 2. 解析消息
            message = self._parse_message(request_data)
            
            # 3. 返回标准格式消息对象
            return {
                "success": True,
                "message": message
            }
        except Exception as e:
            return {"error": f"处理失败: {str(e)}"}
    
    def verify_signature(self, request_data: Dict[str, Any]) -> bool:
        """验证消息签名"""
        # 1. 提取签名
        received_sign = request_data.get("sign")
        if not received_sign:
            return False
        
        # 2. 构建待签名字符串
        # 按照淘宝API签名规则，排除sign字段，将其他参数按字典序排序后拼接
        sorted_params = sorted([(k, v) for k, v in request_data.items() if k != "sign"])
        sign_str = self.app_secret
        for key, value in sorted_params:
            sign_str += f"{key}{value}"
        sign_str += self.app_secret
        
        # 3. 计算签名
        computed_sign = hashlib.md5(sign_str.encode()).hexdigest().upper()
        
        # 4. 验证签名
        return received_sign == computed_sign
    
    def _parse_message(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """解析消息"""
        # 这里根据实际的Webhook消息格式进行解析
        # 示例实现，实际应用中需要根据淘宝的Webhook消息格式进行调整
        return {
            "type": request_data.get("type"),
            "event": request_data.get("event"),
            "buyer_id": request_data.get("buyer_id"),
            "content": request_data.get("content"),
            "timestamp": request_data.get("timestamp"),
            "order_id": request_data.get("order_id")
        }
