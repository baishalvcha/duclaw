#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统配置文件
"""

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Settings(BaseSettings):
    """系统配置"""
    # 淘宝开放平台配置
    TAOBAO_APP_KEY: str = os.getenv("TAOBAO_APP_KEY", "")
    TAOBAO_APP_SECRET: str = os.getenv("TAOBAO_APP_SECRET", "")
    TAOBAO_ACCESS_TOKEN: str = os.getenv("TAOBAO_ACCESS_TOKEN", "")
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./taobao_customer_service.db"
    
    # API服务配置
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    # 其他配置
    PROJECT_NAME: str = "淘宝客服智能接入系统"
    VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"


# 创建配置实例
settings = Settings()
