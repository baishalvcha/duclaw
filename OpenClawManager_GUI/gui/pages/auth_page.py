#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
授权信息页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit,
    QHBoxLayout, QGroupBox, QMessageBox, QSpinBox
)
from PySide6.QtCore import Qt

from gui.language import language_manager
from integration.auth_enhanced import AuthEnhanced


class AuthPage(QWidget):
    """授权信息页面"""
    
    def __init__(self):
        super().__init__()
        self.auth_integration = AuthEnhanced()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        # 标题（根据模式显示不同）
        self.title_label = QLabel(language_manager.get("nav_auth"))
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(self.title_label)
        
        # 批量生成授权码区域（卖家模式）
        batch_group = QGroupBox("批量生成授权码")
        batch_layout = QVBoxLayout(batch_group)
        
        # 数量设置
        count_layout = QHBoxLayout()
        count_label = QLabel("生成数量:")
        count_layout.addWidget(count_label)
        
        self.count_spinbox = QSpinBox()
        self.count_spinbox.setMinimum(1)
        self.count_spinbox.setMaximum(9990)
        self.count_spinbox.setValue(10)
        count_layout.addWidget(self.count_spinbox)
        
        batch_layout.addLayout(count_layout)
        
        # 生成按钮
        generate_button = QPushButton("生成授权码")
        generate_button.clicked.connect(self.generate_batch_codes)
        batch_layout.addWidget(generate_button)
        
        # 生成结果
        self.batch_result_text = QTextEdit()
        self.batch_result_text.setReadOnly(True)
        self.batch_result_text.setFixedHeight(200)
        self.batch_result_text.setPlaceholderText("生成的授权码将显示在这里")
        batch_layout.addWidget(self.batch_result_text)
        
        # 导出按钮
        export_button = QPushButton("导出授权码")
        export_button.clicked.connect(self.export_codes)
        batch_layout.addWidget(export_button)
        
        layout.addWidget(batch_group)
        
        # 机器码区域
        machine_code_group = QGroupBox("机器码")
        machine_code_layout = QVBoxLayout(machine_code_group)
        
        self.machine_code_label = QLabel("正在获取机器码...")
        self.machine_code_label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        self.machine_code_label.setWordWrap(True)
        machine_code_layout.addWidget(self.machine_code_label)
        
        machine_code_buttons = QHBoxLayout()
        copy_button = QPushButton("复制机器码")
        copy_button.clicked.connect(self.copy_machine_code)
        machine_code_buttons.addWidget(copy_button)
        
        refresh_button = QPushButton("刷新")
        refresh_button.clicked.connect(self.refresh_machine_code)
        machine_code_buttons.addWidget(refresh_button)
        
        machine_code_layout.addLayout(machine_code_buttons)
        layout.addWidget(machine_code_group)
        
        # 激活码区域
        activation_group = QGroupBox("激活码")
        activation_layout = QVBoxLayout(activation_group)
        
        activation_label = QLabel("请输入激活码:")
        activation_label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        activation_layout.addWidget(activation_label)
        
        self.activation_code_edit = QTextEdit()
        self.activation_code_edit.setFixedHeight(100)
        self.activation_code_edit.setPlaceholderText("请粘贴激活码")
        activation_layout.addWidget(self.activation_code_edit)
        
        activate_button = QPushButton("激活")
        activate_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 4px;
                padding: 8px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        activate_button.clicked.connect(self.activate)
        activation_layout.addWidget(activate_button)
        layout.addWidget(activation_group)
        
        # 授权状态区域
        status_group = QGroupBox("授权状态")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("未激活")
        self.status_label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        status_layout.addWidget(self.status_label)
        
        check_button = QPushButton("检查授权")
        check_button.clicked.connect(self.check_authorization)
        status_layout.addWidget(check_button)
        layout.addWidget(status_group)
        
        # 初始加载
        self.refresh_machine_code()
        self.check_authorization()
    
    def refresh_machine_code(self):
        """刷新机器码"""
        try:
            machine_code = self.auth_integration.get_machine_code()
            self.machine_code_label.setText(f"机器码: {machine_code}")
        except Exception as e:
            self.machine_code_label.setText(f"获取机器码失败: {str(e)}")
    
    def copy_machine_code(self):
        """复制机器码"""
        machine_code = self.auth_integration.get_machine_code()
        import pyperclip
        pyperclip.copy(machine_code)
        QMessageBox.information(self, "成功", "机器码已复制到剪贴板")
    
    def activate(self):
        """激活"""
        activation_code = self.activation_code_edit.toPlainText().strip()
        if not activation_code:
            QMessageBox.warning(self, "警告", "请输入激活码")
            return
        
        try:
            status, message = self.auth_integration.verify_activation_code(activation_code)
            if status:
                QMessageBox.information(self, "成功", message)
                self.check_authorization()
            else:
                QMessageBox.warning(self, "错误", message)
        except Exception as e:
            QMessageBox.error(self, "错误", f"激活失败: {str(e)}")
    
    def check_authorization(self):
        """检查授权状态"""
        try:
            status, message = self.auth_integration.check_authorization()
            if status:
                self.status_label.setText(f"授权状态: 已激活\n{message}")
                self.status_label.setStyleSheet("font-size: 14px; margin-bottom: 10px; color: #28a745;")
            else:
                self.status_label.setText(f"授权状态: 未激活\n{message}")
                self.status_label.setStyleSheet("font-size: 14px; margin-bottom: 10px; color: #dc3545;")
        except Exception as e:
            self.status_label.setText(f"检查授权失败: {str(e)}")
            self.status_label.setStyleSheet("font-size: 14px; margin-bottom: 10px; color: #dc3545;")
    
    def generate_batch_codes(self):
        """批量生成授权码"""
        count = self.count_spinbox.value()
        try:
            codes = self.auth_integration.generate_batch_license_codes(count)
            # 显示生成的授权码
            codes_text = "\n".join(codes)
            self.batch_result_text.setText(codes_text)
            QMessageBox.information(self, "成功", f"成功生成 {count} 个授权码")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"生成授权码失败: {str(e)}")
    
    def export_codes(self):
        """导出授权码"""
        codes_text = self.batch_result_text.toPlainText().strip()
        if not codes_text:
            QMessageBox.warning(self, "警告", "没有可导出的授权码")
            return
        
        from PySide6.QtWidgets import QFileDialog
        import os
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存授权码文件", "license_codes.txt", "文本文件 (*.txt)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(codes_text)
                QMessageBox.information(self, "成功", f"授权码已导出到: {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"导出失败: {str(e)}")
    
    def update_title(self, mode):
        """根据模式更新标题"""
        if mode == "seller":
            self.title_label.setText("🔑 授权管理")
            # 隐藏买家版的功能，只显示批量生成
            self.buyer_group.hide()
            self.seller_group.show()
        else:
            self.title_label.setText("🔑 授权信息")
            # 隐藏卖家版的功能，只显示激活功能
            self.seller_group.hide()
            self.buyer_group.show()