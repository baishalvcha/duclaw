#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术知识库
"""

from typing import Dict, Any, List, Optional
import sqlite3
import os


class TechKnowledgeBase:
    """技术知识库"""
    
    def __init__(self):
        """初始化技术知识库"""
        # 确保数据目录存在
        os.makedirs('data', exist_ok=True)
        # 连接到SQLite数据库
        self.db_conn = sqlite3.connect('data/tech_knowledge.db')
        # 初始化表结构
        self.initialize_tables()
        # 初始化默认数据
        self.initialize_default_data()
    
    def initialize_tables(self):
        """初始化数据库表"""
        cursor = self.db_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS solutions (
                id INTEGER PRIMARY KEY,
                problem_type TEXT,
                solution TEXT,
                resources TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.db_conn.commit()
    
    def initialize_default_data(self):
        """初始化默认数据"""
        cursor = self.db_conn.cursor()
        # 检查是否已有数据
        cursor.execute("SELECT COUNT(*) FROM solutions")
        if cursor.fetchone()[0] == 0:
            # 添加默认解决方案
            default_solutions = [
                ("installation", "1. 下载并安装最新版本的OpenClaw客户端\n2. 运行安装程序，按照提示完成安装\n3. 启动OpenClaw，登录您的账号\n4. 按照初始化向导完成配置", "https://openclaw.com/docs/installation"),
                ("configuration", "1. 打开OpenClaw设置界面\n2. 在'系统设置'中配置基本参数\n3. 在'网络设置'中配置网络连接\n4. 在'高级设置'中配置高级选项\n5. 保存设置并重启OpenClaw", "https://openclaw.com/docs/configuration"),
                ("error", "1. 检查网络连接是否正常\n2. 重启OpenClaw客户端\n3. 查看日志文件获取详细错误信息\n4. 尝试重新安装最新版本\n5. 如果问题持续，请联系技术支持", "https://openclaw.com/docs/error-codes"),
                ("usage", "1. 查看帮助文档了解基本操作\n2. 参加在线培训课程\n3. 加入社区论坛获取帮助\n4. 查看官方教程视频\n5. 联系技术支持获取个性化指导", "https://openclaw.com/docs/tutorials"),
                ("troubleshooting", "1. 检查系统要求是否满足\n2. 确保使用最新版本\n3. 查看常见问题解答\n4. 尝试重置配置\n5. 联系技术支持获取帮助", "https://openclaw.com/docs/troubleshooting")
            ]
            cursor.executemany(
                "INSERT INTO solutions (problem_type, solution, resources) VALUES (?, ?, ?)",
                default_solutions
            )
            self.db_conn.commit()
    
    async def query(self, problem_type: str) -> str:
        """查询解决方案"""
        # 标准化问题类型
        problem_type = problem_type.lower()
        
        # 映射问题类型到知识库条目
        type_mapping = {
            "安装": "installation",
            "设置": "configuration",
            "配置": "configuration",
            "错误": "error",
            "bug": "error",
            "使用": "usage",
            "教程": "usage",
            "故障": "troubleshooting",
            "问题": "troubleshooting"
        }
        
        # 查找匹配的问题类型
        mapped_type = "troubleshooting"  # 默认类型
        for key, value in type_mapping.items():
            if key in problem_type:
                mapped_type = value
                break
        
        # 从数据库中查询解决方案
        cursor = self.db_conn.cursor()
        cursor.execute(
            "SELECT solution FROM solutions WHERE problem_type = ? ORDER BY created_at DESC LIMIT 1",
            (mapped_type,)
        )
        result = cursor.fetchone()
        return result[0] if result else "请描述具体问题，我帮您分析解决。"
    
    async def add_solution(self, problem_type: str, solution: str, resources: str = ""):
        """添加解决方案"""
        cursor = self.db_conn.cursor()
        cursor.execute(
            "INSERT INTO solutions (problem_type, solution, resources) VALUES (?, ?, ?)",
            (problem_type, solution, resources)
        )
        self.db_conn.commit()
