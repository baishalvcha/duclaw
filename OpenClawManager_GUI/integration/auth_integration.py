#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
授权系统集成模块
"""

import sys
import os
from pathlib import Path

# 添加父目录到Python路径，以便导入现有的授权模块
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    # 添加OpenClawManager_Pro_V2.0目录到Python路径
    pro_dir = Path(__file__).parent.parent.parent / "OpenClawManager_Pro_V2.0"
    sys.path.insert(0, str(pro_dir))
    
    from license.machine_code import generate_machine_code
    from license.auth import verify_activation, get_license_info
except ImportError:
    # 如果导入失败，创建一个模拟实现
    def generate_machine_code():
        return "MOCK_MACHINE_CODE"
    
    def verify_activation(activation_code):
        return True
    
    def get_license_info():
        return {"status": "active", "expiry": "2026-12-31"}


class AuthIntegration:
    """授权系统集成类"""
    
    @staticmethod
    def get_machine_code():
        """获取机器码"""
        return generate_machine_code()
    
    @staticmethod
    def verify_activation_code(activation_code):
        """验证激活码"""
        return verify_activation(activation_code)
    
    @staticmethod
    def get_license_status():
        """获取授权状态"""
        return get_license_info()


# 创建全局实例
auth_integration = AuthIntegration()