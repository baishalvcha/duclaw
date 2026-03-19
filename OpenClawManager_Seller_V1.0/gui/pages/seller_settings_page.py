#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卖家版设置页面 - 简化版
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox,
    QGroupBox, QHBoxLayout, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt


class SellerSettingsPage(QWidget):
    """卖家版设置页面"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        # 标题
        title_label = QLabel("⚙️ 卖家版设置")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)
        
        # 通用设置区域
        general_group = QGroupBox("通用设置")
        general_layout = QVBoxLayout(general_group)
        
        # 开机自启动
        self.auto_start_check = QCheckBox("开机自启动")
        self.auto_start_check.setToolTip("Automatically start with Windows")
        general_layout.addWidget(self.auto_start_check)
        
        # 最小化到托盘
        self.minimize_to_tray_check = QCheckBox("最小化到托盘")
        self.minimize_to_tray_check.setToolTip("Minimize to system tray instead of taskbar")
        general_layout.addWidget(self.minimize_to_tray_check)
        
        # 自动检查更新
        self.auto_update_check = QCheckBox("自动检查更新")
        self.auto_update_check.setToolTip("Automatically check for updates")
        general_layout.addWidget(self.auto_update_check)
        
        # 语言设置
        lang_layout = QHBoxLayout()
        lang_label = QLabel("界面语言:")
        lang_layout.addWidget(lang_label)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("中文", "zh")
        self.lang_combo.addItem("English", "en")
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        
        general_layout.addLayout(lang_layout)
        
        # 保存按钮
        save_btn = QPushButton("保存设置")
        save_btn.setToolTip("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        
        layout.addWidget(general_group)
        layout.addWidget(save_btn)
        
        # 系统信息区域
        info_group = QGroupBox("系统信息")
        info_layout = QVBoxLayout(info_group)
        
        # 版本信息
        version_label = QLabel("版本: 卖家版 V1.0")
        info_layout.addWidget(version_label)
        
        # 版权信息
        copyright_label = QLabel("© 2026 码泓 mahong 版权所有")
        info_layout.addWidget(copyright_label)
        
        # 官方网站
        website_label = QLabel("官方网站: https://mahong.openclaw.ai")
        info_layout.addWidget(website_label)
        
        layout.addWidget(info_group)
        
        layout.addStretch()
        
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
        
        QMessageBox.information(
            self,
            "保存成功",
            "设置已保存成功"
        )