#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
角色处理器基类
"""

from typing import Dict, Any, Optional


class BaseRoleHandler:
    """角色处理器基类"""
    
    async def handle(self, message: Dict[str, Any], context: Dict[str, Any]) -> str:
        """处理消息"""
        raise NotImplementedError("子类必须实现handle方法")
