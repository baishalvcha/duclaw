#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bee销售助理处理器
"""

from typing import Dict, Any, Optional
from .base import BaseRoleHandler


class BeeSalesHandler(BaseRoleHandler):
    """Bee销售助理处理器 - 处理售前相关问题"""
    
    def __init__(self):
        """初始化Bee销售助理处理器"""
        self.name = "Bee"
        self.title = "销售助理"
        self.persona = "26岁月光客服，温暖专业的知心朋友"
        self.product_info = self.load_product_info()
        self.sales_scripts = self.load_sales_scripts()
    
    def load_product_info(self) -> Dict[str, str]:
        """加载产品信息"""
        return {
            "price": "OpenClaw管理器价格：\n个人版：79元\n专业版：199元\n企业定制：请联系客服",
            "feature": "主要功能：\n1. AI助手可视化管理\n2. 多助手协同工作\n3. 自动化工作流\n4. 本地部署安全可靠",
            "purchase": "购买方式：\n1. 淘宝直接下单\n2. 联系客服获取优惠\n3. 企业采购可开发票"
        }
    
    def load_sales_scripts(self) -> Dict[str, str]:
        """加载销售脚本"""
        return {
            "greeting": "您好！我是{name}，{title}～ 😊",
            "closing": "我是您的软件选购顾问，不是推销员。有什么疑问尽管问我，帮您选到最适合的产品～"
        }
    
    def analyze_inquiry(self, content: str) -> str:
        """分析销售咨询类型"""
        content = content.lower()
        
        if "价格" in content or "多少钱" in content or "费用" in content or "价" in content:
            return "price"
        elif "功能" in content or "特点" in content or "特性" in content or "能" in content:
            return "feature"
        elif "购买" in content or "怎么买" in content or "下单" in content or "买" in content:
            return "purchase"
        else:
            return "other"
    
    def get_product_response(self, inquiry_type: str) -> str:
        """获取产品信息回复"""
        if inquiry_type == "price":
            return self.product_info.get("price", "请告诉我您关心：价格、功能还是购买方式？我详细为您介绍～")
        elif inquiry_type == "feature":
            return self.product_info.get("feature", "请告诉我您关心：价格、功能还是购买方式？我详细为您介绍～")
        elif inquiry_type == "purchase":
            return self.product_info.get("purchase", "请告诉我您关心：价格、功能还是购买方式？我详细为您介绍～")
        else:
            return "请告诉我您关心：价格、功能还是购买方式？我详细为您介绍～"
    
    async def handle(self, message: Dict[str, Any], context: Dict[str, Any]) -> str:
        """处理销售咨询"""
        content = message.get("content", "")
        
        # Bee人设化开场
        response = self.sales_scripts["greeting"].format(
            name=self.name, 
            title=self.title
        )
        
        # 分析销售咨询类型
        inquiry_type = self.analyze_inquiry(content)
        
        # 获取产品信息
        product_response = self.get_product_response(inquiry_type)
        
        # 生成Bee风格回复
        response += f"\n\n{product_response}"
        
        # 添加温暖关怀
        response += f"\n\n{self.sales_scripts['closing']}"
        
        return f"【{self.name}】{response}"
