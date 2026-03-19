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
        
        # 启动硬件监控定时器
        from PySide6.QtCore import QTimer
        self.hardware_timer = QTimer()
        self.hardware_timer.timeout.connect(self.update_hardware_monitor)
        self.hardware_timer.start(5000)  # 每5秒更新一次
        
        # 初始更新一次
        self.update_hardware_monitor()
    
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
        
        # 添加硬件监控信号灯区域
        hardware_monitor_widget = QWidget()
        hardware_monitor_widget.setStyleSheet("""
            background-color: #2d2d2d;
            border-radius: 6px;
            padding: 8px;
            margin-bottom: 10px;
        """)
        hardware_layout = QVBoxLayout(hardware_monitor_widget)
        hardware_layout.setContentsMargins(5, 5, 5, 5)
        hardware_layout.setSpacing(4)
        
        # 监控标题
        monitor_title = QLabel("系统状态监控")
        monitor_title.setStyleSheet("""
            color: #00aaff;
            font-weight: bold;
            font-size: 11px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 1px;
        """)
        hardware_layout.addWidget(monitor_title)
        
        # 信号灯容器
        signal_container = QWidget()
        signal_layout = QHBoxLayout(signal_container)
        signal_layout.setContentsMargins(0, 0, 0, 0)
        signal_layout.setSpacing(8)
        
        # 硬件监控项目
        hardware_items = [
            ("CPU", "🟢", "CPU使用率: 45% | 温度: 65°C"),
            ("内存", "🟢", "内存: 8GB/16GB (50%)"),
            ("硬盘", "🟡", "硬盘: 256GB/512GB (50%)"),
            ("网关", "🟢", "网关: 在线 | 延迟: 15ms"),
            ("网络", "🟢", "网络: 已连接 | 速度: 100Mbps"),
            ("系统", "🟢", "系统负载: 正常 | 进程: 45个"),
        ]
        
        self.hardware_labels = {}
        for name, status, tooltip in hardware_items:
            item_widget = QWidget()
            item_layout = QVBoxLayout(item_widget)
            item_layout.setContentsMargins(0, 0, 0, 0)
            item_layout.setSpacing(2)
            item_layout.setAlignment(Qt.AlignCenter)
            
            # 信号灯
            status_label = QLabel(status)
            status_label.setStyleSheet("""
                font-size: 14px;
                font-weight: bold;
            """)
            status_label.setToolTip(tooltip)
            
            # 名称
            name_label = QLabel(name)
            name_label.setStyleSheet("""
                color: #ffffff;
                font-size: 9px;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            """)
            name_label.setToolTip(tooltip)
            
            item_layout.addWidget(status_label)
            item_layout.addWidget(name_label)
            signal_layout.addWidget(item_widget)
            
            self.hardware_labels[name] = (status_label, name_label)
        
        hardware_layout.addWidget(signal_container)
        nav_layout.addWidget(hardware_monitor_widget)
        
        # 添加分隔线
        separator1 = QWidget()
        separator1.setFixedHeight(1)
        separator1.setStyleSheet("background-color: #444;")
        nav_layout.addWidget(separator1)
        
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
                background-color: white;
                color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #333;
                margin-right: 5px;
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
        # 在标题前添加Logo字符
        logo = "🦐 "  # 使用虾emoji作为临时Logo，稍后替换为图片
        if self.current_mode == "buyer":
            self.setWindowTitle(f"{logo}码泓mahong-openclaw管理器-买家版V1.0")
        else:
            self.setWindowTitle(f"{logo}码泓mahong-openclaw管理器-卖家版V1.0")
    
    def update_hardware_monitor(self):
        """更新硬件监控状态"""
        if not hasattr(self, 'hardware_labels'):
            return
        
        import random
        import time
        
        # 模拟硬件状态数据
        hardware_data = {
            "CPU": {
                "usage": random.randint(20, 80),
                "temp": random.randint(50, 85),
                "status": random.choice(["normal", "warning", "critical"])
            },
            "内存": {
                "usage": random.randint(30, 90),
                "total": 16,
                "status": random.choice(["normal", "warning", "critical"])
            },
            "硬盘": {
                "usage": random.randint(40, 95),
                "total": 512,
                "status": random.choice(["normal", "warning", "critical"])
            },
            "网关": {
                "online": random.random() > 0.1,  # 90%在线概率
                "latency": random.randint(10, 100) if random.random() > 0.1 else 0,
                "status": "normal" if random.random() > 0.1 else "critical"
            },
            "网络": {
                "connected": random.random() > 0.05,  # 95%连接概率
                "speed": random.randint(50, 200) if random.random() > 0.05 else 0,
                "status": "normal" if random.random() > 0.05 else "critical"
            },
            "系统": {
                "load": round(random.uniform(0.5, 3.0), 2),
                "processes": random.randint(30, 80),
                "status": random.choice(["normal", "warning", "critical"])
            }
        }
        
        # 状态对应的emoji和颜色
        status_map = {
            "normal": ("🟢", "#00ff00"),
            "warning": ("🟡", "#ffff00"),
            "critical": ("🔴", "#ff0000")
        }
        
        # 更新每个硬件项
        for name, data in hardware_data.items():
            if name in self.hardware_labels:
                status_label, name_label = self.hardware_labels[name]
                status_emoji, color = status_map[data["status"]]
                
                # 更新信号灯
                status_label.setText(status_emoji)
                status_label.setStyleSheet(f"""
                    font-size: 14px;
                    font-weight: bold;
                    color: {color};
                """)
                
                # 更新工具提示
                tooltip = ""
                if name == "CPU":
                    tooltip = f"CPU: {data['usage']}%使用率 | 温度: {data['temp']}°C"
                elif name == "内存":
                    used = int(data['total'] * data['usage'] / 100)
                    tooltip = f"内存: {used}GB/{data['total']}GB ({data['usage']}%)"
                elif name == "硬盘":
                    used = int(data['total'] * data['usage'] / 100)
                    tooltip = f"硬盘: {used}GB/{data['total']}GB ({data['usage']}%)"
                elif name == "网关":
                    tooltip = f"网关: {'在线' if data['online'] else '离线'} | 延迟: {data['latency']}ms"
                elif name == "网络":
                    tooltip = f"网络: {'已连接' if data['connected'] else '断开连接'} | 速度: {data['speed']}Mbps"
                elif name == "系统":
                    tooltip = f"系统负载: {data['load']} | 进程数: {data['processes']}"
                
                status_label.setToolTip(tooltip)
                name_label.setToolTip(tooltip)
    
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