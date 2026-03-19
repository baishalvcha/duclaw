#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
授权管理模块
统一买家版授权系统
根据授权码确定版本（基础版、专业版）
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple


class AuthManager:
    """授权管理器"""
    
    def __init__(self, config_dir: str = None):
        """
        初始化授权管理器
        
        Args:
            config_dir: 配置文件目录，默认为用户目录下的 .mahong
        """
        if config_dir is None:
            # 使用用户目录下的 .mahong 文件夹
            home_dir = os.path.expanduser("~")
            self.config_dir = os.path.join(home_dir, ".mahong")
        else:
            self.config_dir = config_dir
            
        # 确保配置目录存在
        os.makedirs(self.config_dir, exist_ok=True)
        
        # 授权文件路径
        self.auth_file = os.path.join(self.config_dir, "auth.json")
        
        # 加载授权信息
        self.auth_info = self._load_auth_info()
        
        # 版本功能定义
        self.feature_definitions = {
            "trial": {
                "name": "试用版",
                "features": self._get_trial_features(),
                "expiry_days": 30,
            },
            "basic": {
                "name": "基础版",
                "features": self._get_basic_features(),
                "expiry_days": None,  # 永久
            },
            "pro": {
                "name": "专业版",
                "features": self._get_pro_features(),
                "expiry_days": None,  # 永久
            }
        }
    
    def _load_auth_info(self) -> Dict:
        """加载授权信息"""
        if os.path.exists(self.auth_file):
            try:
                with open(self.auth_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._get_default_auth_info()
        else:
            return self._get_default_auth_info()
    
    def _save_auth_info(self):
        """保存授权信息"""
        with open(self.auth_file, 'w', encoding='utf-8') as f:
            json.dump(self.auth_info, f, ensure_ascii=False, indent=2)
    
    def _get_default_auth_info(self) -> Dict:
        """获取默认授权信息（未授权状态）"""
        return {
            "license_key": None,
            "license_type": "trial",  # 默认试用版
            "activated": False,
            "activation_date": None,
            "expiry_date": None,
            "machine_id": self._get_machine_id(),
            "features": self._get_trial_features()
        }
    
    def _get_machine_id(self) -> str:
        """获取机器标识（简化版）"""
        import platform
        import hashlib
        
        # 使用主机名和用户名生成机器ID
        machine_info = f"{platform.node()}-{os.getlogin()}"
        return hashlib.md5(machine_info.encode()).hexdigest()[:16]
    
    def _get_trial_features(self) -> Dict[str, bool]:
        """试用版功能"""
        return {
            "install_openclaw": True,
            "basic_monitoring": True,
            "simple_config": True,
            "basic_diagnostics": True,
            "status_monitoring": True,
            "update_checks": True,
            "batch_operations": False,      # 试用版禁用
            "advanced_analytics": False,    # 试用版禁用
            "automation_workflows": False,  # 试用版禁用
            "multi_account_support": False, # 试用版禁用
            "data_export": False,           # 试用版禁用
            "performance_dashboard": False, # 试用版禁用
        }
    
    def _get_basic_features(self) -> Dict[str, bool]:
        """基础版功能"""
        features = self._get_trial_features().copy()
        # 基础版在试用版基础上没有额外功能
        # 但标记为已授权状态
        return features
    
    def _get_pro_features(self) -> Dict[str, bool]:
        """专业版功能"""
        features = self._get_trial_features().copy()
        # 专业版启用所有高级功能
        features.update({
            "batch_operations": True,
            "advanced_analytics": True,
            "automation_workflows": True,
            "multi_account_support": True,
            "data_export": True,
            "performance_dashboard": True,
        })
        return features
    
    def validate_license_key(self, license_key: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        验证授权码
        
        Args:
            license_key: 授权码
            
        Returns:
            (是否有效, 错误信息, 授权信息)
        """
        # 清理授权码
        license_key = license_key.strip().upper()
        
        # 检查授权码格式
        if not license_key:
            return False, "授权码不能为空", None
        
        # 模拟授权码验证（实际应连接服务器验证）
        # 这里使用简单的本地验证逻辑
        
        # 试用版授权码（30天试用）
        if license_key.startswith("MAHONG-TRIAL-"):
            auth_info = {
                "license_key": license_key,
                "license_type": "trial",
                "activated": True,
                "activation_date": datetime.now().isoformat(),
                "expiry_date": (datetime.now() + timedelta(days=30)).isoformat(),
                "machine_id": self._get_machine_id(),
                "features": self._get_trial_features()
            }
            return True, "试用版授权成功（30天）", auth_info
        
        # 基础版授权码
        elif license_key.startswith("MAHONG-BASIC-"):
            auth_info = {
                "license_key": license_key,
                "license_type": "basic",
                "activated": True,
                "activation_date": datetime.now().isoformat(),
                "expiry_date": None,  # 永久
                "machine_id": self._get_machine_id(),
                "features": self._get_basic_features()
            }
            return True, "基础版授权成功", auth_info
        
        # 专业版授权码
        elif license_key.startswith("MAHONG-PRO-"):
            auth_info = {
                "license_key": license_key,
                "license_type": "pro",
                "activated": True,
                "activation_date": datetime.now().isoformat(),
                "expiry_date": None,  # 永久
                "machine_id": self._get_machine_id(),
                "features": self._get_pro_features()
            }
            return True, "专业版授权成功", auth_info
        
        # 测试授权码（开发用）
        elif license_key == "TEST-BASIC-1234":
            auth_info = {
                "license_key": license_key,
                "license_type": "basic",
                "activated": True,
                "activation_date": datetime.now().isoformat(),
                "expiry_date": None,
                "machine_id": self._get_machine_id(),
                "features": self._get_basic_features()
            }
            return True, "测试版（基础版）授权成功", auth_info
        
        elif license_key == "TEST-PRO-1234":
            auth_info = {
                "license_key": license_key,
                "license_type": "pro",
                "activated": True,
                "activation_date": datetime.now().isoformat(),
                "expiry_date": None,
                "machine_id": self._get_machine_id(),
                "features": self._get_pro_features()
            }
            return True, "测试版（专业版）授权成功", auth_info
        
        else:
            return False, "无效的授权码格式", None
    
    def activate_license(self, license_key: str) -> Tuple[bool, str]:
        """
        激活授权
        
        Args:
            license_key: 授权码
            
        Returns:
            (是否成功, 消息)
        """
        valid, message, auth_info = self.validate_license_key(license_key)
        
        if valid and auth_info:
            # 更新授权信息
            self.auth_info.update(auth_info)
            self._save_auth_info()
            return True, message
        else:
            return False, message
    
    def get_current_license_info(self) -> Dict:
        """获取当前授权信息"""
        return self.auth_info.copy()
    
    def get_license_type(self) -> str:
        """获取当前授权类型"""
        return self.auth_info.get("license_type", "trial")
    
    def get_license_name(self) -> str:
        """获取授权类型名称"""
        license_type = self.get_license_type()
        return self.feature_definitions.get(license_type, {}).get("name", "试用版")
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """检查功能是否启用"""
        features = self.auth_info.get("features", {})
        return features.get(feature_name, False)
    
    def is_activated(self) -> bool:
        """检查是否已授权"""
        return self.auth_info.get("activated", False)
    
    def is_trial_expired(self) -> bool:
        """检查试用版是否过期"""
        if self.get_license_type() != "trial":
            return False
            
        expiry_date_str = self.auth_info.get("expiry_date")
        if not expiry_date_str:
            return False
            
        try:
            expiry_date = datetime.fromisoformat(expiry_date_str)
            return datetime.now() > expiry_date
        except:
            return False
    
    def get_remaining_days(self) -> Optional[int]:
        """获取剩余天数（仅试用版）"""
        if self.get_license_type() != "trial":
            return None
            
        expiry_date_str = self.auth_info.get("expiry_date")
        if not expiry_date_str:
            return None
            
        try:
            expiry_date = datetime.fromisoformat(expiry_date_str)
            remaining = (expiry_date - datetime.now()).days
            return max(0, remaining)
        except:
            return None
    
    def reset_to_trial(self):
        """重置为试用版"""
        self.auth_info = self._get_default_auth_info()
        self._save_auth_info()


# 全局授权管理器实例
_auth_manager = None

def get_auth_manager() -> AuthManager:
    """获取全局授权管理器实例"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager


if __name__ == "__main__":
    # 测试代码
    auth = AuthManager()
    
    print("当前授权状态:")
    print(f"  授权类型: {auth.get_license_name()}")
    print(f"  是否激活: {auth.is_activated()}")
    print(f"  功能列表:")
    
    for feature, enabled in auth.auth_info.get("features", {}).items():
        print(f"    {feature}: {'✅' if enabled else '❌'}")
    
    # 测试授权码
    test_keys = [
        "TEST-BASIC-1234",
        "TEST-PRO-1234",
        "MAHONG-TRIAL-ABCD-EFGH-IJKL",
        "INVALID-KEY"
    ]
    
    print("\n授权码测试:")
    for key in test_keys:
        success, message, _ = auth.validate_license_key(key)
        print(f"  {key}: {'✅' if success else '❌'} {message}")