#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理器
"""

import os
import yaml
from typing import Dict, Any, Optional


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config/config.yaml"):
        """初始化配置管理器"""
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "taobao": {
                "app_key": "",
                "app_secret": "",
                "sandbox": True,
                "webhook_url": "https://your-domain.com/api/v1/webhook/taobao"
            },
            "server": {
                "host": "0.0.0.0",
                "port": 8000,
                "debug": False,
                "workers": 4
            },
            "database": {
                "path": "data/tscs.db",
                "backup_dir": "backups"
            },
            "logging": {
                "level": "INFO",
                "file": "logs/tscs.log",
                "max_size_mb": 100
            }
        }
    
    def save_config(self) -> None:
        """保存配置"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()
