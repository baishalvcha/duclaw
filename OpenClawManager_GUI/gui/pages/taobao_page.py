#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
淘宝自动发货页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QTextEdit, QFileDialog, QMessageBox, QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal
import os

from gui.language import language_manager


class TaobaoPage(QWidget):
    """淘宝自动发货页面"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel(language_manager.get("nav_taobao"))
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # 描述
        desc_label = QLabel("生成淘宝自动发货文件，包含授权码信息")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # 授权码输入
        auth_code_label = QLabel("授权码列表:")
        layout.addWidget(auth_code_label)
        
        self.auth_code_text = QTextEdit()
        self.auth_code_text.setPlaceholderText("每行一个授权码")
        self.auth_code_text.setMinimumHeight(200)
        layout.addWidget(self.auth_code_text)
        
        # 按钮组
        button_layout = QHBoxLayout()
        
        import_button = QPushButton("导入授权码")
        import_button.clicked.connect(self.import_auth_codes)
        button_layout.addWidget(import_button)
        
        generate_button = QPushButton("生成发货文件")
        generate_button.clicked.connect(self.generate_delivery_file)
        button_layout.addWidget(generate_button)
        
        layout.addLayout(button_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 结果显示
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(100)
        layout.addWidget(self.result_text)
        
        self.setLayout(layout)
    
    def import_auth_codes(self):
        """导入授权码文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择授权码文件", "", "文本文件 (*.txt)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.auth_code_text.setText(content)
                QMessageBox.information(self, "成功", "授权码导入成功")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"导入失败: {str(e)}")
    
    def generate_delivery_file(self):
        """生成淘宝自动发货文件"""
        auth_codes = self.auth_code_text.toPlainText().strip().split('\n')
        auth_codes = [code.strip() for code in auth_codes if code.strip()]
        
        if not auth_codes:
            QMessageBox.warning(self, "警告", "请输入授权码")
            return
        
        # 生成发货文件
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存发货文件", "taobao_delivery.txt", "文本文件 (*.txt)"
        )
        if file_path:
            try:
                # 淘宝自动发货文件格式：每行一个授权码
                with open(file_path, 'w', encoding='utf-8') as f:
                    for code in auth_codes:
                        f.write(f"{code}\n")
                
                self.result_text.setText(f"发货文件生成成功！\n文件路径: {file_path}\n生成授权码数量: {len(auth_codes)}")
                QMessageBox.information(self, "成功", "发货文件生成成功")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"生成失败: {str(e)}")