#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通道管理页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QTextEdit
)
from PySide6.QtCore import Qt


class ChannelPage(QWidget):
    """通道管理页面"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 通道配置工具区域
        tool_group = QGroupBox("通道配置工具")
        tool_layout = QVBoxLayout(tool_group)
        
        btn_layout = QHBoxLayout()
        self.launch_btn = QPushButton("启动通道配置工具")
        self.launch_btn.clicked.connect(self.launch_config_tool)
        self.view_btn = QPushButton("查看当前配置")
        self.view_btn.clicked.connect(self.view_config)
        btn_layout.addWidget(self.launch_btn)
        btn_layout.addWidget(self.view_btn)
        tool_layout.addLayout(btn_layout)
        
        # 通道类型说明区域
        info_group = QGroupBox("通道类型说明")
        info_layout = QVBoxLayout(info_group)
        
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setPlainText("通道类型说明:\n\n" 
                                   "1. 本地通道：直接连接本地OpenClaw服务\n" 
                                   "2. 远程通道：连接远程OpenClaw服务\n" 
                                   "3. 代理通道：通过代理服务器连接OpenClaw\n" 
                                   "4. 集群通道：连接多节点OpenClaw集群")
        info_layout.addWidget(self.info_text)
        
        layout.addWidget(tool_group)
        layout.addWidget(info_group)
        layout.addStretch()
    
    def launch_config_tool(self):
        """启动通道配置工具"""
        # 这里将启动现有的Tkinter通道配置工具
        print("启动通道配置工具")
    
    def view_config(self):
        """查看当前配置"""
        # 这里将显示当前通道配置
        print("查看当前配置")