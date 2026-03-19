#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卖家版主窗口类 - 独立版本
"""

import os
import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QMenuBar, QMenu, QSystemTrayIcon, QMessageBox
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap

from gui.pages.seller_auth_page import SellerAuthPage
from gui.pages.seller_settings_page import SellerSettingsPage
from gui.pages.seller_help_page import SellerHelpPage


class SellerMainWindow(QMainWindow):
    """卖家版主窗口类"""

    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        # 设置窗口大小
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowTitle("码泓mahong-openclaw管理器-卖家版V1.0")
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建左侧导航栏
        self.nav_widget = QWidget()
        self.nav_widget.setFixedWidth(220)
        self.nav_widget.setStyleSheet("""
            background-color: #f0f0f0;
            border-right: 1px solid #ddd;
        """)
        nav_layout = QVBoxLayout(self.nav_widget)
        nav_layout.setContentsMargins(10, 20, 10, 20)
        nav_layout.setSpacing(10)
        
        # 卖家版标题
        title_label = QLabel("卖家版 V1.0")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #28a745; margin-bottom: 10px;")
        nav_layout.addWidget(title_label)
        
        # 添加分隔线
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #ddd;")
        nav_layout.addWidget(separator)
        
        # 卖家版导航按钮
        nav_buttons = [
            ("🔑 授权管理", "Authorization Management", self.show_auth_page),
            ("⚙️ 设置", "Settings", self.show_settings_page),
            ("🆘 帮助", "Help", self.show_help_page),
        ]
        
        self.nav_buttons = []
        for text, tooltip, callback in nav_buttons:
            button = QPushButton(text)
            button.setToolTip(tooltip)
            button.setFixedHeight(40)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    text-align: left;
                    padding-left: 15px;
                }
                QPushButton:hover {
                    background-color: #e6f2ff;
                    border-color: #0078d7;
                }
            """)
            button.clicked.connect(callback)
            nav_layout.addWidget(button)
            self.nav_buttons.append(button)
        
        # 添加拉伸空间
        nav_layout.addStretch()
        
        # 创建右侧内容区
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        
        # 添加到主布局
        main_layout.addWidget(self.nav_widget)
        main_layout.addWidget(self.content_widget)
        
        # 初始化页面
        self.pages = {
            "auth": SellerAuthPage(),
            "settings": SellerSettingsPage(),
            "help": SellerHelpPage(),
        }
        
        # 显示授权管理页面
        self.show_auth_page()
    
    def show_auth_page(self):
        """显示授权管理页面"""
        self.show_page("auth")
    
    def show_settings_page(self):
        """显示设置页面"""
        self.show_page("settings")
    
    def show_help_page(self):
        """显示帮助页面"""
        self.show_page("help")
    
    def show_page(self, page_name):
        """显示指定页面"""
        # 清空内容区
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.hide()
                self.content_layout.removeWidget(widget)
        
        # 显示新页面
        page = self.pages.get(page_name)
        if page:
            self.content_layout.addWidget(page)
            page.show()
    
    def show_about(self):
        """显示关于对话框"""
        # 读取版本信息
        version_info = self.get_version_info()
        
        about_text = f"""
{version_info['product_name']}

一款专为卖家设计的授权码批量管理工具
支持批量生成、导出和管理授权码

版本信息：
• 外部版本：{version_info['external_version']}
• 内部版本：{version_info['internal_version']}
• 构建日期：{version_info['build_date']}
• 构建类型：{version_info['build_type']}

{version_info['copyright']}
官方网站：{version_info['website']}
技术支持QQ群：{version_info['support_qq']}
"""
        
        QMessageBox.about(
            self,
            "关于卖家版",
            about_text.strip()
        )
    
    def get_version_info(self):
        """获取版本信息"""
        version_file = os.path.join(os.path.dirname(__file__), '..', 'VERSION')
        version_info = {
            'product_name': '码泓mahong-openclaw管理器-卖家版',
            'external_version': 'V1.0.0',
            'internal_version': '1.0.0+build.20260318.001',
            'build_date': '2026-03-18',
            'build_type': 'development',
            'copyright': '© 2026 码泓 mahong 版权所有',
            'website': 'https://mahong.openclaw.ai',
            'support_qq': '123456789'
        }
        
        try:
            if os.path.exists(version_file):
                with open(version_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('VERSION='):
                            version_info['external_version'] = 'V' + line.split('=')[1]
                        elif line.startswith('BUILD_VERSION='):
                            version_info['internal_version'] = line.split('=')[1]
                        elif line.startswith('BUILD_DATE='):
                            version_info['build_date'] = line.split('=')[1]
                        elif line.startswith('BUILD_TYPE='):
                            version_info['build_type'] = line.split('=')[1]
                        elif line.startswith('COPYRIGHT='):
                            version_info['copyright'] = line.split('=')[1]
                        elif line.startswith('WEBSITE='):
                            version_info['website'] = line.split('=')[1]
                        elif line.startswith('SUPPORT_QQ='):
                            version_info['support_qq'] = line.split('=')[1]
        except Exception as e:
            print(f"读取版本文件失败: {e}")
        
        return version_info