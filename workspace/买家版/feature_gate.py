#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能开关模块
根据授权类型控制功能可用性
"""

# 导入授权管理模块
try:
    from auth_manager import get_auth_manager
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from auth_manager import get_auth_manager


class FeatureGate:
    """功能开关管理器"""
    
    def __init__(self):
        self.auth_manager = get_auth_manager()
        
        # 功能权限映射
        self._feature_permissions = {
            # 安装管理相关
            "install_openclaw": ["trial", "basic", "pro"],
            "uninstall_openclaw": ["trial", "basic", "pro"],
            "update_openclaw": ["trial", "basic", "pro"],
            
            # 基础监控
            "basic_monitoring": ["trial", "basic", "pro"],
            "status_dashboard": ["trial", "basic", "pro"],
            "system_health": ["trial", "basic", "pro"],
            
            # 配置管理
            "simple_config": ["trial", "basic", "pro"],
            "basic_settings": ["trial", "basic", "pro"],
            
            # 诊断工具
            "basic_diagnostics": ["trial", "basic", "pro"],
            "error_logs": ["trial", "basic", "pro"],
            
            # 更新检查
            "update_checks": ["trial", "basic", "pro"],
            "version_check": ["trial", "basic", "pro"],
            
            # === 专业版功能 ===
            
            # 批量操作
            "batch_operations": ["pro"],
            "batch_install": ["pro"],
            "batch_config": ["pro"],
            
            # 高级分析
            "advanced_analytics": ["pro"],
            "performance_metrics": ["pro"],
            "usage_statistics": ["pro"],
            
            # 自动化工作流
            "automation_workflows": ["pro"],
            "scheduled_tasks": ["pro"],
            "trigger_actions": ["pro"],
            
            # 多账户支持
            "multi_account_support": ["pro"],
            "account_switching": ["pro"],
            "profile_management": ["pro"],
            
            # 数据导出
            "data_export": ["pro"],
            "export_logs": ["pro"],
            "export_configs": ["pro"],
            "export_statistics": ["pro"],
            
            # 性能仪表盘
            "performance_dashboard": ["pro"],
            "real_time_monitoring": ["pro"],
            "historical_data": ["pro"],
            
            # 高级配置
            "advanced_config": ["pro"],
            "expert_settings": ["pro"],
            "custom_scripts": ["pro"],
        }
    
    def is_enabled(self, feature_name: str) -> bool:
        """
        检查功能是否可用
        
        Args:
            feature_name: 功能名称
            
        Returns:
            是否可用
        """
        # 首先检查授权管理器的功能开关
        if self.auth_manager.is_feature_enabled(feature_name):
            return True
        
        # 然后检查功能权限映射
        allowed_versions = self._feature_permissions.get(feature_name, [])
        current_version = self.auth_manager.get_license_type()
        
        return current_version in allowed_versions
    
    def get_enabled_features(self) -> list:
        """获取所有可用的功能"""
        enabled_features = []
        for feature_name in self._feature_permissions.keys():
            if self.is_enabled(feature_name):
                enabled_features.append(feature_name)
        return enabled_features
    
    def get_disabled_features(self) -> list:
        """获取所有禁用的功能"""
        disabled_features = []
        for feature_name in self._feature_permissions.keys():
            if not self.is_enabled(feature_name):
                disabled_features.append(feature_name)
        return disabled_features
    
    def get_features_by_category(self) -> dict:
        """按类别获取功能状态"""
        categories = {
            "安装管理": ["install_openclaw", "uninstall_openclaw", "update_openclaw"],
            "基础监控": ["basic_monitoring", "status_dashboard", "system_health"],
            "配置管理": ["simple_config", "basic_settings"],
            "诊断工具": ["basic_diagnostics", "error_logs"],
            "更新检查": ["update_checks", "version_check"],
            "批量操作": ["batch_operations", "batch_install", "batch_config"],
            "高级分析": ["advanced_analytics", "performance_metrics", "usage_statistics"],
            "自动化": ["automation_workflows", "scheduled_tasks", "trigger_actions"],
            "多账户": ["multi_account_support", "account_switching", "profile_management"],
            "数据导出": ["data_export", "export_logs", "export_configs", "export_statistics"],
            "性能仪表盘": ["performance_dashboard", "real_time_monitoring", "historical_data"],
            "高级配置": ["advanced_config", "expert_settings", "custom_scripts"],
        }
        
        result = {}
        for category, features in categories.items():
            category_features = []
            for feature in features:
                category_features.append({
                    "name": feature,
                    "enabled": self.is_enabled(feature),
                    "description": self._get_feature_description(feature)
                })
            result[category] = category_features
        
        return result
    
    def _get_feature_description(self, feature_name: str) -> str:
        """获取功能描述"""
        descriptions = {
            "install_openclaw": "一键安装OpenClaw",
            "uninstall_openclaw": "卸载OpenClaw",
            "update_openclaw": "更新OpenClaw版本",
            "basic_monitoring": "基础系统监控",
            "status_dashboard": "状态仪表盘",
            "system_health": "系统健康检查",
            "simple_config": "简单配置管理",
            "basic_settings": "基础设置",
            "basic_diagnostics": "基础诊断工具",
            "error_logs": "错误日志查看",
            "update_checks": "更新检查",
            "version_check": "版本检查",
            "batch_operations": "批量操作功能",
            "batch_install": "批量安装",
            "batch_config": "批量配置",
            "advanced_analytics": "高级数据分析",
            "performance_metrics": "性能指标",
            "usage_statistics": "使用统计",
            "automation_workflows": "自动化工作流",
            "scheduled_tasks": "计划任务",
            "trigger_actions": "触发动作",
            "multi_account_support": "多账户支持",
            "account_switching": "账户切换",
            "profile_management": "配置文件管理",
            "data_export": "数据导出功能",
            "export_logs": "导出日志",
            "export_configs": "导出配置",
            "export_statistics": "导出统计",
            "performance_dashboard": "性能仪表盘",
            "real_time_monitoring": "实时监控",
            "historical_data": "历史数据",
            "advanced_config": "高级配置选项",
            "expert_settings": "专家设置",
            "custom_scripts": "自定义脚本",
        }
        
        return descriptions.get(feature_name, "未知功能")
    
    def get_license_summary(self) -> dict:
        """获取授权摘要"""
        auth_manager = self.auth_manager
        auth_info = auth_manager.get_current_license_info()
        
        return {
            "license_type": auth_info.get("license_type", "trial"),
            "license_name": auth_manager.get_license_name(),
            "activated": auth_info.get("activated", False),
            "activation_date": auth_info.get("activation_date"),
            "expiry_date": auth_info.get("expiry_date"),
            "remaining_days": auth_manager.get_remaining_days(),
            "total_features": len(self._feature_permissions),
            "enabled_features": len(self.get_enabled_features()),
            "disabled_features": len(self.get_disabled_features()),
        }


# 全局功能开关实例
_feature_gate = None

def get_feature_gate() -> FeatureGate:
    """获取全局功能开关实例"""
    global _feature_gate
    if _feature_gate is None:
        _feature_gate = FeatureGate()
    return _feature_gate


if __name__ == "__main__":
    # 测试代码
    feature_gate = FeatureGate()
    
    print("功能开关测试:")
    print(f"当前授权类型: {feature_gate.auth_manager.get_license_name()}")
    print(f"是否激活: {feature_gate.auth_manager.is_activated()}")
    print()
    
    # 测试几个关键功能
    test_features = [
        "install_openclaw",
        "batch_operations",
        "advanced_analytics",
        "automation_workflows",
        "data_export",
        "performance_dashboard"
    ]
    
    print("功能状态测试:")
    for feature in test_features:
        enabled = feature_gate.is_enabled(feature)
        print(f"  {feature}: {'✅ 可用' if enabled else '❌ 不可用'}")
    
    print()
    
    # 获取授权摘要
    summary = feature_gate.get_license_summary()
    print("授权摘要:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print()
    
    # 按类别显示功能
    print("按类别功能状态:")
    categories = feature_gate.get_features_by_category()
    for category, features in categories.items():
        print(f"\n{category}:")
        for feature in features:
            status = "✅" if feature["enabled"] else "❌"
            print(f"  {status} {feature['name']} - {feature['description']}")