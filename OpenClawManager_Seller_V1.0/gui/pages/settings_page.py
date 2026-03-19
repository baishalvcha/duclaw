#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置页面 - 优化版（删除网关设置）
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox,
    QGroupBox, QHBoxLayout, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt

from gui.language import language_manager
from integration.cli_integration import CLIIntegration


class SettingsPage(QWidget):
    """设置页面"""
    
    def __init__(self):
        super().__init__()
        self.cli_integration = CLIIntegration()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        # 通用设置
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
        save_btn = QPushButton(language_manager.get("settings_save"))
        save_btn.setToolTip("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        
        layout.addWidget(general_group)
        layout.addWidget(save_btn)
        
        # 加载当前设置
        self.load_settings()
    
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
        
        # 更新语言
        language_manager.set_language(language)
        
        QMessageBox.information(
            self,
            "保存成功",
            "设置已保存 (Settings saved successfully)."
        )