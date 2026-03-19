#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent管理页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QListWidget, QListWidgetItem, QGroupBox, QComboBox
)
from PySide6.QtCore import Qt


class AgentPage(QWidget):
    """Agent管理页面"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 创建Agent区域
        create_group = QGroupBox("创建Agent")
        create_layout = QHBoxLayout(create_group)
        
        name_label = QLabel("Agent名称:")
        self.name_edit = QLineEdit()
        type_label = QLabel("Agent类型:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["通用型", "专业型", "自定义"])
        create_btn = QPushButton("创建")
        create_btn.clicked.connect(self.create_agent)
        
        create_layout.addWidget(name_label)
        create_layout.addWidget(self.name_edit)
        create_layout.addWidget(type_label)
        create_layout.addWidget(self.type_combo)
        create_layout.addWidget(create_btn)
        
        # Agent列表区域
        list_group = QGroupBox("Agent列表")
        list_layout = QVBoxLayout(list_group)
        
        self.agent_list = QListWidget()
        list_layout.addWidget(self.agent_list)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        self.manage_btn = QPushButton("管理Agent")
        self.manage_btn.clicked.connect(self.manage_agent)
        btn_layout.addWidget(self.manage_btn)
        list_layout.addLayout(btn_layout)
        
        layout.addWidget(create_group)
        layout.addWidget(list_group)
        layout.addStretch()
    
    def create_agent(self):
        """创建Agent"""
        name = self.name_edit.text()
        agent_type = self.type_combo.currentText()
        
        if name:
            item = QListWidgetItem(f"{name} ({agent_type})")
            item.setData(Qt.UserRole, {
                "name": name,
                "type": agent_type
            })
            self.agent_list.addItem(item)
            # 清空输入
            self.name_edit.clear()
    
    def manage_agent(self):
        """管理Agent"""
        selected_item = self.agent_list.currentItem()
        if selected_item:
            agent_data = selected_item.data(Qt.UserRole)
            # 这里将集成现有的Agent管理功能
            print(f"管理Agent: {agent_data['name']}")