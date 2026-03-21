#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
"""

import os
import sqlite3


def init_directories():
    """初始化必要的目录"""
    directories = [
        "data",
        "logs",
        "backups",
        "config"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"创建目录: {directory}")


def init_tech_knowledge_db():
    """初始化技术知识库数据库"""
    db_path = "data/tech_knowledge.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建解决方案表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solutions (
            id INTEGER PRIMARY KEY,
            problem_type TEXT,
            solution TEXT,
            resources TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
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
        print("添加默认解决方案数据")
    
    conn.commit()
    conn.close()
    print(f"初始化技术知识库数据库: {db_path}")


def init_tscs_db():
    """初始化系统主数据库"""
    db_path = "data/tscs.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id TEXT UNIQUE,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建消息表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            message_id TEXT UNIQUE,
            user_id TEXT,
            content TEXT,
            intent TEXT,
            role TEXT,
            response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # 创建性能表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance (
            id INTEGER PRIMARY KEY,
            response_time REAL,
            intent_accuracy REAL,
            role_effectiveness REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"初始化系统主数据库: {db_path}")


def main():
    """主函数"""
    print("开始初始化数据库...")
    init_directories()
    init_tech_knowledge_db()
    init_tscs_db()
    print("数据库初始化完成！")


if __name__ == "__main__":
    main()
