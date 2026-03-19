#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
买家版主窗口类 - 独立版本
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QMenuBar, QMenu, QSystemTrayIcon, QMessageBox
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap

from gui.language import language_manager
from gui.pages.home_page import HomePage
from gui.pages.install_page import InstallPage
from gui.pages.model_page import ModelPage
from gui.pages.channel_page import ChannelPage
from gui.pages.buyer_settings_page import BuyerSettingsPage
from gui.pages.help_page import HelpPage
from gui.pages.logs_page import LogsPage


class BuyerMainWindow(QMainWindow):
    """买家版主窗口类"""

    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        # 设置窗口大小
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowTitle("码泓mahong-openclaw管理器-买家版V1.0")
        
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
        
        # 买家版标题
        title_label = QLabel("买家版 V1.0")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #0078d7; margin-bottom: 10px;")
        nav_layout.addWidget(title_label)
        
        # 添加分隔线
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #ddd;")
        nav_layout.addWidget(separator)
        
        # 买家版导航按钮
        nav_buttons = [
            ("🏠 首页", "Home", self.show_home_page),
            ("🚀 安装/卸载", "Install/Uninstall", self.show_install_page),
            ("🤖 模型管理", "Model Management", self.show_model_page),
            ("📱 通道管理", "Channel Management", self.show_channel_page),
            ("⚙️ 设置", "Settings", self.show_settings_page),
            ("📋 日志监控", "Logs", self.show_logs_page),
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
            "home": HomePage(),
            "install": InstallPage(),
            "model": ModelPage(),
            "channel": ChannelPage(),
            "settings": BuyerSettingsPage(),
            "logs": LogsPage(),
            "help": HelpPage(),
        }
        
        # 显示首页
        self.show_home_page()
    
    def show_home_page(self):
        """显示首页"""
        self.show_page("home")
    
    def show_install_page(self):
        """显示安装/卸载页面"""
        self.show_page("install")
    
    def show_model_page(self):
        """显示模型管理页面"""
        self.show_page("model")
    
    def show_channel_page(self):
        """显示通道管理页面"""
        self.show_page("channel")
    
    def show_settings_page(self):
        """显示设置页面"""
        self.show_page("settings")
    
    def show_logs_page(self):
        """显示日志监控页面"""
        self.show_page("logs")
    
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
        QMessageBox.about(
            self,
            "关于买家版",
            "码泓mahong-openclaw管理器-买家版V1.0\n\n"
            "一款专为个人用户设计的OpenClaw可视化管理工具\n"
            "支持一键安装、模型管理、通道配置等功能\n\n"
            "© 2026 码泓 mahong 版权所有\n"
            "版本：v1.0 (2026-03-18)\n"
            "官方网站：https://mahong.openclaw.ai"
        )
