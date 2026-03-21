#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Judy技术专家处理器
"""

from typing import Dict, Any, Optional
from .base import BaseRoleHandler
from src.knowledge_base.tech_knowledge import TechKnowledgeBase


class JudyTechHandler(BaseRoleHandler):
    """Judy技术专家处理器 - 处理售后相关问题"""
    
    def __init__(self):
        """初始化Judy技术专家处理器"""
        self.name = "Judy"
        self.title = "OpenClaw技术专家"
        self.knowledge_base = TechKnowledgeBase()
        self.response_templates = self.load_templates()
    
    def load_templates(self) -> Dict[str, str]:
        """加载响应模板"""
        return {
            "greeting": "我是{name}，{title}。",
            "solution": "根据我的经验，建议这样处理：\n{solution}",
            "resources": "相关资源：{resources}",
            "follow_up": "这个问题我负责跟进，确保解决。有问题随时找我。"
        }
    
    def analyze_problem(self, content: str) -> str:
        """分析技术问题类型"""
        content = content.lower()
        
        if "安装" in content or "setup" in content:
            return "安装"
        elif "配置" in content or "设置" in content or "config" in content:
            return "配置"
        elif "错误" in content or "bug" in content or "error" in content:
            return "错误"
        elif "使用" in content or "教程" in content or "usage" in content or "guide" in content:
            return "使用"
        elif "问题" in content or "故障" in content or "problem" in content:
            return "问题"
        else:
            return "其他"
    
    def get_resources(self, problem_type: str) -> str:
        """获取相关资源链接"""
        resources = {
            "安装": "https://openclaw.com/docs/installation",
            "配置": "https://openclaw.com/docs/configuration",
            "错误": "https://openclaw.com/docs/error-codes",
            "使用": "https://openclaw.com/docs/tutorials",
            "问题": "https://openclaw.com/docs/troubleshooting"
        }
        return resources.get(problem_type, "https://openclaw.com/docs")
    
    def format_solution(self, solution: str) -> str:
        """Judy风格的问题解决方案格式化"""
        return self.response_templates["solution"].format(solution=solution)
    
    async def handle(self, message: Dict[str, Any], context: Dict[str, Any]) -> str:
        """处理技术咨询"""
        content = message.get("content", "")
        
        # Judy人设化开场
        response = self.response_templates["greeting"].format(
            name=self.name, 
            title=self.title
        )
        
        # 分析技术问题类型
        problem_type = self.analyze_problem(content)
        
        # 查询知识库
        solution = await self.knowledge_base.query(problem_type)
        
        # 生成Judy风格回复
        response += f"\n\n{self.format_solution(solution)}"
        
        # 添加资源链接
        resources = self.get_resources(problem_type)
        response += f"\n\n{self.response_templates['resources'].format(resources=resources)}"
        
        # 添加跟进承诺
        response += f"\n\n{self.response_templates['follow_up']}"
        
        return f"【{self.name}】{response}"
