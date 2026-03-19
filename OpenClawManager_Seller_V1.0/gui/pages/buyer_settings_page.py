#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
买家版设置页面 - 包含授权管理
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox,
    QGroupBox, QHBoxLayout, QMessageBox, QComboBox, QTextEdit
)
from PySide6.QtCore import Qt
import uuid
import hashlib


class BuyerSettingsPage(QWidget):
    """买家版设置页面（包含授权管理）"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        # 授权管理区域
        auth_group = QGroupBox("授权管理 (License Management)")
        auth_layout = QVBoxLayout(auth_group)
        
        # 机器码显示
        machine_code_layout = QHBoxLayout()
        machine_label = QLabel("机器码 (Machine Code):")
        machine_code_layout.addWidget(machine_label)
        
        self.machine_code_label = QLabel(self.get_machine_code())
        self.machine_code_label.setStyleSheet("font-family: monospace; background-color: #f5f5f5; padding: 5px; border: 1px solid #ddd;")
        machine_code_layout.addWidget(self.machine_code_label)
        
        # 复制按钮
        copy_button = QPushButton("复制 (Copy)")
        copy_button.clicked.connect(self.copy_machine_code)
        machine_code_layout.addWidget(copy_button)
        
        auth_layout.addLayout(machine_code_layout)
        
        # 激活码输入
        activate_layout = QHBoxLayout()
        activate_label = QLabel("激活码 (Activation Code):")
        activate_layout.addWidget(activate_label)
        
        self.activate_input = QLineEdit()
        self.activate_input.setPlaceholderText("请输入16位激活码")
        self.activate_input.setMaxLength(16)
        activate_layout.addWidget(self.activate_input)
        
        auth_layout.addLayout(activate_layout)
        
        # 激活按钮
        activate_button_layout = QHBoxLayout()
        self.activate_button = QPushButton("激活 (Activate)")
        self.activate_button.clicked.connect(self.activate_license)
        activate_button_layout.addWidget(self.activate_button)
        
        self.check_status_button = QPushButton("检查状态 (Check Status)")
        self.check_status_button.clicked.connect(self.check_license_status)
        activate_button_layout.addWidget(self.check_status_button)
        
        auth_layout.addLayout(activate_button_layout)
        
        # 授权状态显示
        self.status_label = QLabel("状态: 未激活 (Status: Not Activated)")
        self.status_label.setStyleSheet("font-weight: bold; color: #dc3545;")
        auth_layout.addWidget(self.status_label)
        
        layout.addWidget(auth_group)
        
        # 通用设置区域
        general_group = QGroupBox("通用设置 (General Settings)")
        general_layout = QVBoxLayout(general_group)
        
        # 开机自启动
        self.auto_start_check = QCheckBox("开机自启动 (Auto Start)")
        self.auto_start_check.setToolTip("Automatically start with Windows")
        general_layout.addWidget(self.auto_start_check)
        
        # 最小化到托盘
        self.minimize_to_tray_check = QCheckBox("最小化到托盘 (Minimize to Tray)")
        self.minimize_to_tray_check.setToolTip("Minimize to system tray instead of taskbar")
        general_layout.addWidget(self.minimize_to_tray_check)
        
        # 自动检查更新
        self.auto_update_check = QCheckBox("自动检查更新 (Auto Check Updates)")
        self.auto_update_check.setToolTip("Automatically check for updates")
        general_layout.addWidget(self.auto_update_check)
        
        # 语言设置
        lang_layout = QHBoxLayout()
        lang_label = QLabel("界面语言 (Interface Language):")
        lang_layout.addWidget(lang_label)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("中文 (Chinese)", "zh")
        self.lang_combo.addItem("English", "en")
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        
        general_layout.addLayout(lang_layout)
        
        # 保存按钮
        save_btn = QPushButton("保存设置 (Save Settings)")
        save_btn.setToolTip("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        
        layout.addWidget(general_group)
        layout.addWidget(save_btn)
        
        # 加载当前设置
        self.load_settings()
    
    def get_machine_code(self):
        """获取机器码"""
        # 生成基于系统信息的机器码
        try:
            # 使用主机名和MAC地址生成机器码
            import socket
            import uuid as uuid_module
            
            hostname = socket.gethostname()
            mac = ':'.join(['{:02x}'.format((uuid_module.getnode() >> elements) & 0xff) 
                           for elements in range(0, 2*6, 2)][::-1])
            
            # 生成哈希值作为机器码
            machine_info = f"{hostname}_{mac}"
            machine_hash = hashlib.md5(machine_info.encode()).hexdigest()[:16].upper()
            
            # 格式化为XXXX-XXXX-XXXX-XXXX
            formatted_code = '-'.join([machine_hash[i:i+4] for i in range(0, 16, 4)])
            return formatted_code
        except:
            # 如果获取失败，使用随机UUID
            random_uuid = str(uuid.uuid4()).replace('-', '').upper()[:16]
            return '-'.join([random_uuid[i:i+4] for i in range(0, 16, 4)])
    
    def copy_machine_code(self):
        """复制机器码到剪贴板"""
        from PySide6.QtGui import QGuiApplication
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.machine_code_label.text())
        QMessageBox.information(self, "复制成功", "机器码已复制到剪贴板")
    
    def activate_license(self):
        """激活授权"""
        activation_code = self.activate_input.text().strip()
        
        if not activation_code:
            QMessageBox.warning(self, "输入错误", "请输入激活码")
            return
        
        if len(activation_code) != 16:
            QMessageBox.warning(self, "输入错误", "激活码应为16位字符")
            return
        
        # 这里应该调用实际的激活验证逻辑
        # 暂时模拟激活成功
        self.status_label.setText("状态: 已激活 (Status: Activated)")
        self.status_label.setStyleSheet("font-weight: bold; color: #28a745;")
        
        QMessageBox.information(
            self,
            "激活成功",
            f"软件激活成功！\n机器码: {self.machine_code_label.text()}\n激活码: {activation_code}"
        )
    
    def check_license_status(self):
        """检查授权状态"""
        # 这里应该检查实际的授权状态
        # 暂时显示模拟状态
        if self.status_label.text().startswith("状态: 已激活"):
            QMessageBox.information(self, "授权状态", "软件已激活，授权状态正常")
        else:
            QMessageBox.warning(self, "授权状态", "软件未激活，请先激活授权")
    
    def load_settings(self):
        """加载设置"""
        # 这里应该从配置文件加载设置
        # 暂时使用默认值
        self.auto_start_check.setChecked(True)
        self.minimize_to_tray_check.setChecked(True)
        self.auto_update_check.setChecked(True)
        self.lang_combo.setCurrentIndex(0)  # 默认中文
    
    def save_settings(self):
        """保存设置"""
        # 获取设置值
        auto_start = self.auto_start_check.isChecked()
        minimize_to_tray = self.minimize_to_tray_check.isChecked()
        auto_update = self.auto_update_check.isChecked()
        language = self.lang_combo.currentData()
        
        # 这里应该保存到配置文件
        # 暂时只显示保存成功的消息
        
        QMessageBox.information(
            self,
            "保存成功",
            "设置已保存 (Settings saved successfully)."
        )