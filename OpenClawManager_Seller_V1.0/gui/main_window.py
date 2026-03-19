#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口类
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QMenuBar, QMenu, QSystemTrayIcon, QMessageBox, QComboBox
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap

from gui.language import language_manager
from gui.pages.home_page import HomePage
from gui.pages.auth_page import AuthPage
from gui.pages.install_page import InstallPage
from gui.pages.model_page import ModelPage
from gui.pages.channel_page import ChannelPage
from gui.pages.settings_page import SettingsPage
from gui.pages.help_page import HelpPage
from gui.pages.logs_page import LogsPage


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.current_mode = "buyer"  # 默认买家模式
        self.init_ui()
        self.init_tray()
    
    def init_ui(self):
        """初始化界面"""
        # 设置窗口大小
        self.setGeometry(100, 100, 1200, 800)
        self.update_window_title()
        
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
        
        # 添加模式切换下拉框（去掉标签）
        self.mode_combo = QComboBox()
        self.mode_combo.addItem(language_manager.get("mode_buyer"), "buyer")
        self.mode_combo.addItem(language_manager.get("mode_seller"), "seller")
        self.mode_combo.setCurrentIndex(0)  # 默认选择买家模式
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        self.mode_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        nav_layout.addWidget(self.mode_combo)
        
        # 添加分隔线
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #ddd;")
        nav_layout.addWidget(separator)
        
        # 添加导航按钮
        nav_buttons = [
            (language_manager.get("nav_home"), "Home", self.show_home_page),
            (language_manager.get("nav_auth") + " (License Code)", "Authorization", self.show_auth_page),
            (language_manager.get("nav_install"), "Install/Uninstall", self.show_install_page),
            (language_manager.get("nav_model") + " (Model)", "Model Management", self.show_model_page),
            (language_manager.get("nav_channel") + " (Channel)", "Channel Management", self.show_channel_page),
            (language_manager.get("nav_agent") + " (Agent)", "Agent Management", self.show_agent_page),
            (language_manager.get("nav_settings") + " (Settings)", "Settings", self.show_settings_page),
            (language_manager.get("nav_help"), "Help", self.show_help_page),
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
                QPushButton:pressed {
                    background-color: #cce6ff;
                }
            """)
            button.clicked.connect(callback)
            nav_layout.addWidget(button)
            self.nav_buttons.append(button)
        
        nav_layout.addStretch()
        
        # 创建右侧内容区
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        
        # 添加到主布局
        main_layout.addWidget(self.nav_widget)
        main_layout.addWidget(self.content_widget)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 初始化页面
        self.pages = {
            "home": HomePage(),
            "auth": AuthPage(),
            "install": InstallPage(),
            "model": ModelPage(),
            "channel": ChannelPage(),
            "settings": SettingsPage(),
            "logs": LogsPage(),
            "help": HelpPage(),
        }
        
        # 显示首页
        self.show_home_page()
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = self.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu(language_manager.get("menu_file"))
        exit_action = QAction(language_manager.get("menu_exit"), self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 工具菜单
        tool_menu = menu_bar.addMenu(language_manager.get("menu_tool"))
        
        # 添加工具菜单项
        config_action = QAction(language_manager.get("menu_config"), self)
        tool_menu.addAction(config_action)
        
        restart_action = QAction(language_manager.get("menu_restart"), self)
        tool_menu.addAction(restart_action)
        
        tool_menu.addSeparator()
        
        clear_cache_action = QAction(language_manager.get("menu_clear_cache"), self)
        tool_menu.addAction(clear_cache_action)
        
        # 帮助菜单
        help_menu = menu_bar.addMenu(language_manager.get("menu_help"))
        about_action = QAction(language_manager.get("menu_about"), self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        help_action = QAction(language_manager.get("menu_usage_help"), self)
        help_action.triggered.connect(self.show_help_page)
        help_menu.addAction(help_action)
    
    def init_tray(self):
        """初始化系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        # 尝试加载图标，如果不存在则使用默认图标
        try:
            icon_path = "assets/icons/icon.png"
            self.tray_icon.setIcon(QIcon(icon_path))
        except:
            # 使用默认图标
            self.tray_icon.setIcon(QIcon())
        
        tray_menu = QMenu()
        show_action = QAction(language_manager.get("tray_show"), self)
        show_action.triggered.connect(self.show)
        exit_action = QAction(language_manager.get("tray_exit"), self)
        exit_action.triggered.connect(self.close)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # 连接系统托盘信号
        self.tray_icon.activated.connect(self.on_tray_activated)
    
    def on_tray_activated(self, reason):
        """系统托盘激活事件"""
        if reason == QSystemTrayIcon.Trigger:
            # 左键点击托盘图标
            if self.isHidden():
                self.show()
            else:
                self.hide()
    
    def show_home_page(self):
        """显示首页"""
        self.show_page("home")
    
    def show_auth_page(self):
        """显示授权信息页面"""
        self.show_page("auth")
        # 更新授权页面的标题
        auth_page = self.pages.get("auth")
        if auth_page and hasattr(auth_page, 'update_title'):
            auth_page.update_title(self.current_mode)
    
    def show_install_page(self):
        """显示安装/卸载页面"""
        self.show_page("install")
    
    def show_model_page(self):
        """显示模型管理页面"""
        self.show_page("model")
    
    def show_channel_page(self):
        """显示通道管理页面"""
        self.show_page("channel")
    
    def show_agent_page(self):
        """显示Agent管理页面"""
        self.show_page("agent")
    
    def show_settings_page(self):
        """显示设置页面"""
        self.show_page("settings")
    
    def show_help_page(self):
        """显示帮助页面"""
        self.show_page("help")
    
    def on_mode_changed(self, index):
        """模式切换事件处理"""
        new_mode = self.mode_combo.itemData(index)
        if new_mode != self.current_mode:
            self.current_mode = new_mode
            self.update_window_title()  # 更新窗口标题
            self.update_navigation()
            # 显示首页
            self.show_home_page()
    
    def update_navigation(self):
        """根据当前模式更新导航"""
        # 清空导航按钮
        for button in self.nav_buttons:
            button.hide()
            self.nav_widget.layout().removeWidget(button)
        
        # 根据模式重新添加导航按钮
        if self.current_mode == "seller":
            # 卖家模式导航按钮（优化版）
            nav_buttons = [
                ("🔑 授权管理", "Authorization Management", self.show_auth_page),
                (language_manager.get("nav_settings") + " (Settings)", "Settings", self.show_settings_page),
                (language_manager.get("nav_help"), "Help", self.show_help_page),
            ]
        else:
            # 买家模式导航按钮（优化版）
            nav_buttons = [
                (language_manager.get("nav_home"), "Home", self.show_home_page),
                (language_manager.get("nav_install"), "Install/Uninstall", self.show_install_page),
                (language_manager.get("nav_model") + " (Model)", "Model Management", self.show_model_page),
                (language_manager.get("nav_channel") + " (Channel)", "Channel Management", self.show_channel_page),
                (language_manager.get("nav_settings") + " (Settings)", "Settings", self.show_settings_page),
                ("📋 日志监控 (Logs)", "Logs", self.show_logs_page),
                (language_manager.get("nav_help"), "Help", self.show_help_page),
            ]
        
        # 添加新的导航按钮
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
                QPushButton:pressed {
                    background-color: #cce6ff;
                }
            """)
            button.clicked.connect(callback)
            self.nav_widget.layout().addWidget(button)
            self.nav_buttons.append(button)
        
        # 添加拉伸空间
        self.nav_widget.layout().addStretch()
    
    def show_logs_page(self):
        """显示日志监控页面"""
        self.show_page("logs")
    
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
    
    def update_window_title(self):
        """更新窗口标题"""
        if self.current_mode == "buyer":
            self.setWindowTitle("码泓mahong-openclaw管理器-买家版V1.0")
        else:
            self.setWindowTitle("码泓mahong-openclaw管理器-卖家版V1.0")
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self,
            language_manager.get("about_title"),
            language_manager.get("about_content")
        )
    
    def closeEvent(self, event):
        """关闭事件"""
        # 最小化到托盘
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "码泓mahong-OpenClaw管理器",
            "应用已最小化到系统托盘",
            QSystemTrayIcon.Information,
            2000
        )