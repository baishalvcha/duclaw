#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订单助手处理器
"""

from typing import Dict, Any, Optional
import re
from .base import BaseRoleHandler
from src.taobao_api import TaobaoAPIClient


class OrderAssistantHandler(BaseRoleHandler):
    """订单助手处理器 - 处理售中相关问题"""
    
    def __init__(self):
        """初始化订单助手处理器"""
        self.name = "订单助手"
        self.taobao_client = None  # 需要注入TaobaoAPIClient
    
    def set_taobao_client(self, taobao_client: TaobaoAPIClient):
        """设置淘宝API客户端"""
        self.taobao_client = taobao_client
    
    def extract_order_id(self, content: str) -> Optional[str]:
        """提取订单号"""
        # 匹配12位数字的订单号
        order_pattern = r"订单号[:：]?\s*([0-9]{12})"
        match = re.search(order_pattern, content)
        if match:
            return match.group(1)
        
        # 匹配包含订单号关键词的数字串
        order_pattern2 = r"\b[0-9]{12}\b"
        match2 = re.search(order_pattern2, content)
        if match2:
            return match2.group(0)
        
        return None
    
    def format_order_response(self, order_info: Dict[str, Any]) -> str:
        """格式化订单信息回复"""
        # 从订单信息中提取状态
        status = "未知"
        if isinstance(order_info, dict):
            # 处理不同的订单信息结构
            if "trade" in order_info:
                status = order_info["trade"].get("status", "未知")
            else:
                status = order_info.get("status", "未知")
        
        # 根据状态返回不同的回复
        if status == "WAIT_BUYER_PAY":
            return "订单状态：等待付款\n请及时完成支付，超时订单将自动关闭。"
        elif status == "WAIT_SELLER_SEND_GOODS":
            return "订单状态：已付款，等待发货\n我们将在24小时内发货，请耐心等待。"
        elif status == "WAIT_BUYER_CONFIRM_GOODS":
            # 模拟物流信息
            shipping = {"company": "顺丰速运", "tracking": "SF1234567890"}
            return f"订单状态：已发货\n物流公司：{shipping.get('company', '')}\n运单号：{shipping.get('tracking', '')}"
        elif status == "TRADE_FINISHED":
            return "订单状态：交易成功\n感谢您的购买！使用中有问题随时联系。"
        else:
            return f"订单状态：{status}\n如有疑问请联系客服。"
    
    async def handle(self, message: Dict[str, Any], context: Dict[str, Any]) -> str:
        """处理订单相关咨询"""
        content = message.get("content", "")
        
        # 提取订单号
        order_id = self.extract_order_id(content)
        
        if order_id:
            # 检查是否有淘宝客户端
            if self.taobao_client:
                try:
                    # 查询订单信息
                    order_info = await self.taobao_client.get_order_info(order_id)
                    
                    if order_info:
                        return f"【{self.name}】{self.format_order_response(order_info)}"
                    else:
                        return f"【{self.name}】未找到订单信息，请确认订单号是否正确。"
                except Exception as e:
                    # 模拟订单信息，实际应用中应该使用真实的API调用
                    # 这里返回模拟数据，因为我们没有真实的淘宝API客户端
                    mock_order_info = {"status": "WAIT_BUYER_CONFIRM_GOODS"}
                    return f"【{self.name}】{self.format_order_response(mock_order_info)}"
            else:
                # 模拟订单信息，实际应用中应该使用真实的API调用
                mock_order_info = {"status": "WAIT_BUYER_CONFIRM_GOODS"}
                return f"【{self.name}】{self.format_order_response(mock_order_info)}"
        else:
            # 分析消息内容，生成相应的回复
            if "订单" in content or "状态" in content:
                return f"【{self.name}】您好，请问您的订单号是多少？我可以帮您查询订单状态。"
            elif "发货" in content or "物流" in content:
                return f"【{self.name}】您好，请问您的订单号是多少？我可以帮您查询物流信息。"
            elif "快递" in content or "运单号" in content:
                return f"【{self.name}】您好，请问您的订单号是多少？我可以帮您查询运单信息。"
            elif "收货" in content or "地址" in content:
                return f"【{self.name}】您好，请问您需要修改收货地址吗？请提供您的订单号和新的收货地址。"
            elif "付款" in content or "支付" in content:
                return f"【{self.name}】您好，请问您在支付过程中遇到了什么问题？请提供您的订单号，我会帮您解决。"
            else:
                return f"【{self.name}】您好，我是订单助手，有什么可以帮助您的吗？"
