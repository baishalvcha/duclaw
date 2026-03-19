#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型管理页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QListWidget, QListWidgetItem, QGroupBox, QGridLayout
)
from PySide6.QtCore import Qt


class ModelPage(QWidget):
    """模型管理页面"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 添加模型区域
        add_group = QGroupBox("添加AI模型")
        add_layout = QGridLayout(add_group)
        add_layout.setSpacing(10)
        
        # 模型名称
        add_layout.addWidget(QLabel("模型名称:"), 0, 0)
        self.model_name_edit = QLineEdit()
        add_layout.addWidget(self.model_name_edit, 0, 1, 1, 3)
        
        # 提供商
        add_layout.addWidget(QLabel("提供商:"), 1, 0)
        self.provider_edit = QLineEdit()
        add_layout.addWidget(self.provider_edit, 1, 1, 1, 3)
        
        # API Key
        add_layout.addWidget(QLabel("API Key:"), 2, 0)
        self.api_key_edit = QLineEdit()
        add_layout.addWidget(self.api_key_edit, 2, 1, 1, 3)
        
        # Base URL
        add_layout.addWidget(QLabel("Base URL:"), 3, 0)
        self.base_url_edit = QLineEdit()
        add_layout.addWidget(self.base_url_edit, 3, 1, 1, 3)
        
        # 添加按钮
        add_btn = QPushButton("添加模型")
        add_btn.clicked.connect(self.add_model)
        add_layout.addWidget(add_btn, 4, 0, 1, 4)
        
        # 模型列表区域
        list_group = QGroupBox("模型列表")
        list_layout = QVBoxLayout(list_group)
        
        self.model_list = QListWidget()
        list_layout.addWidget(self.model_list)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        self.test_btn = QPushButton("测试连接")
        self.test_btn.clicked.connect(self.test_model)
        self.delete_btn = QPushButton("删除模型")
        self.delete_btn.clicked.connect(self.delete_model)
        btn_layout.addWidget(self.test_btn)
        btn_layout.addWidget(self.delete_btn)
        list_layout.addLayout(btn_layout)
        
        layout.addWidget(add_group)
        layout.addWidget(list_group)
        layout.addStretch()
    
    def add_model(self):
        """添加模型"""
        name = self.model_name_edit.text()
        provider = self.provider_edit.text()
        api_key = self.api_key_edit.text()
        base_url = self.base_url_edit.text()
        
        if name and provider:
            item = QListWidgetItem(f"{name} - {provider}")
            item.setData(Qt.UserRole, {
                "name": name,
                "provider": provider,
                "api_key": api_key,
                "base_url": base_url
            })
            self.model_list.addItem(item)
            # 清空输入
            self.model_name_edit.clear()
            self.provider_edit.clear()
            self.api_key_edit.clear()
            self.base_url_edit.clear()
    
    def test_model(self):
        """测试模型连接"""
        selected_item = self.model_list.currentItem()
        if selected_item:
            model_data = selected_item.data(Qt.UserRole)
            # 这里将集成现有的模型测试功能
            print(f"测试模型: {model_data['name']}")
    
    def delete_model(self):
        """删除模型"""
        selected_item = self.model_list.currentItem()
        if selected_item:
            self.model_list.takeItem(self.model_list.row(selected_item))