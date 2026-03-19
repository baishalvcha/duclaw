#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
首页
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt


class HomePage(QWidget):
    """首页"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        # 标题
        title_label = QLabel("欢迎使用码泓mahong-OpenClaw管理器")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)
        
        # 简介
        intro_label = QLabel(
            "这是一款一键安装/绿化版的OpenClaw可视化管理工具，面向非技术用户，提供图形化操作界面。\n\n" 
            "主要功能：\n" 
            "• 无需命令行操作\n" 
            "• 无需代码知识\n" 
            "• 纯本地运行，数据安全\n" 
            "• 绿色免安装，删除即卸载"
        )
        intro_label.setStyleSheet("font-size: 14px; line-height: 1.5; margin-bottom: 30px;")
        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)
        
        # 快速操作按钮
        quick_actions = QHBoxLayout()
        quick_actions.setSpacing(20)
        
        install_button = QPushButton("🚀 安装OpenClaw")
        install_button.setFixedHeight(50)
        install_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        quick_actions.addWidget(install_button)
        
        model_button = QPushButton("🤖 管理模型")
        model_button.setFixedHeight(50)
        model_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1e7e34;
            }
        """)
        quick_actions.addWidget(model_button)
        
        settings_button = QPushButton("⚙️ 系统设置")
        settings_button.setFixedHeight(50)
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: #333;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        quick_actions.addWidget(settings_button)
        
        layout.addLayout(quick_actions)
        
        # 系统状态
        status_label = QLabel("系统状态")
        status_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 40px; margin-bottom: 15px;")
        layout.addWidget(status_label)
        
        status_info = QLabel(
            "• OpenClaw: 未安装\n" 
            "• 授权状态: 未激活\n" 
            "• 模型数量: 0\n" 
            "• 通道数量: 0\n" 
            "• Agent数量: 0"
        )
        status_info.setStyleSheet("font-size: 14px; line-height: 1.5;")
        layout.addWidget(status_info)
        
        # 版本信息
        version_label = QLabel("版本: v1.0")
        version_label.setStyleSheet("font-size: 12px; color: #666; margin-top: 40px;")
        layout.addWidget(version_label)