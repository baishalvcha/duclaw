#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
淘宝开放平台API客户端
"""

from typing import Dict, Any, Optional
import requests
import json
from datetime import datetime


class TaobaoAPIClient:
    """淘宝开放平台API客户端"""
    
    def __init__(self, app_key: str, app_secret: str, session_key: str = None):
        """初始化淘宝API客户端"""
        self.app_key = app_key
        self.app_secret = app_secret
        self.session_key = session_key
        self.gateway_url = "https://eco.taobao.com/router/rest"
    
    def _build_sign(self, params: Dict[str, Any]) -> str:
        """构建签名"""
        # 实际应用中需要根据淘宝API的签名规则实现
        # 这里只是一个示例
        import hashlib
        sorted_params = sorted(params.items())
        sign_str = self.app_secret
        for key, value in sorted_params:
            sign_str += f"{key}{value}"
        sign_str += self.app_secret
        return hashlib.md5(sign_str.encode()).hexdigest().upper()
    
    def call_api(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """调用淘宝API"""
        # 构建请求参数
        req_params = {
            "app_key": self.app_key,
            "method": method,
            "format": "json",
            "v": "2.0",
            "sign_method": "md5",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **params
        }
        
        # 如果有session_key，添加到参数中
        if self.session_key:
            req_params["session"] = self.session_key
        
        # 计算签名
        req_params["sign"] = self._build_sign(req_params)
        
        # 发送请求
        response = requests.get(self.gateway_url, params=req_params)
        
        # 处理响应
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API调用失败: {response.status_code}"}
    
    def send_message(self, buyer_id: str, content: str, msg_type: str = "text") -> Dict[str, Any]:
        """发送消息给买家"""
        return self.call_api(
            "taobao.message.send",
            {
                "receiver_id": buyer_id,
                "content": content,
                "type": msg_type
            }
        )
    
    def get_order_info(self, tid: str) -> Dict[str, Any]:
        """获取订单信息"""
        return self.call_api(
            "taobao.trade.get",
            {
                "fields": "tid,status,payment,total_fee,post_fee,buyer_nick,buyer_id",
                "tid": tid
            }
        )
    
    def get_buyer_info(self, buyer_id: str) -> Dict[str, Any]:
        """获取买家信息"""
        return self.call_api(
            "taobao.user.get",
            {
                "fields": "user_id,nick,sex,buyer_credit",
                "user_id": buyer_id
            }
        )
