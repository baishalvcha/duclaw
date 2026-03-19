#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
码泓mahong-OpenClaw管理器 v1.0（GUI版） - 修复版本
主程序入口
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QLocale, QTranslator

# 简化版本的主窗口
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QMenuBar, QMenu, QSystemTrayIcon, QComboBox
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap


class SimpleMainWindow(QMainWindow):
    """简化版本的主窗口 - 用于测试"""
    
    def __init__(self):
        super().__init__()
        self.current_mode = "buyer"  # 默认买家模式
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        # 设置窗口大小
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowTitle("码泓mahong-OpenClaw管理器 v2.0 - 测试版")
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建左侧导航栏
        nav_widget = QWidget()
        nav_widget.setFixedWidth(200)
        nav_widget.setStyleSheet("""
            background-color: #f0f0f0;
            border-right: 1px solid #ddd;
        """)
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(10, 20, 10, 20)
        nav_layout.setSpacing(10)
        
        # 添加模式切换
        mode_label = QLabel("模式切换")
        mode_label.setStyleSheet("font-weight: bold;")
        nav_layout.addWidget(mode_label)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("买家模式", "buyer")
        self.mode_combo.addItem("卖家模式", "seller")
        self.mode_combo.setCurrentIndex(0)
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        nav_layout.addWidget(self.mode_combo)
        
        # 添加分隔线
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #ddd;")
        nav_layout.addWidget(separator)
        
        # 添加导航按钮 - 简化版本
        nav_buttons = [
            ("🏠 首页", self.show_home),
            ("🔑 授权信息", self.show_auth),
            ("🚀 安装/卸载", self.show_install),
            ("🤖 模型管理", self.show_model),
            ("📱 通道管理", self.show_channel),
            ("👥 Agent管理", self.show_agent),
            ("⚙️ 设置", self.show_settings),
            ("📋 日志监控", self.show_logs),
            ("🆘 帮助", self.show_help),
        ]
        
        for text, callback in nav_buttons:
            button = QPushButton(text)
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
        
        nav_layout.addStretch()
        
        # 创建右侧内容区
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        
        # 添加到主布局
        main_layout.addWidget(nav_widget)
        main_layout.addWidget(self.content_widget)
        
        # 显示欢迎信息
        self.show_welcome()
    
    def show_welcome(self):
        """显示欢迎信息"""
        self.clear_content()
        
        welcome_label = QLabel("欢迎使用码泓mahong-OpenClaw管理器 v2.0")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #0078d7;")
        self.content_layout.addWidget(welcome_label)
        
        info_label = QLabel("""
        <p>这是一个简化测试版本，用于验证按钮点击功能。</p>
        <p>当前模式：<b>买家模式</b></p>
        <p>请点击左侧导航按钮测试功能。</p>
        <p>如果按钮可以正常点击，说明基础功能正常。</p>
        """)
        info_label.setStyleSheet("font-size: 14px; margin-top: 20px;")
        self.content_layout.addWidget(info_label)
        
        self.content_layout.addStretch()
    
    def clear_content(self):
        """清空内容区"""
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.hide()
                self.content_layout.removeWidget(widget)
    
    def on_mode_changed(self, index):
        """模式切换"""
        new_mode = self.mode_combo.itemData(index)
        QMessageBox.information(self, "模式切换", f"已切换到{new_mode}模式")
        self.current_mode = new_mode
    
    def show_home(self):
        self.show_page("🏠 首页", "这是首页内容")
    
    def show_auth(self):
        self.show_page("🔑 授权信息", "授权信息页面 - 功能正常")
    
    def show_install(self):
        self.show_page("🚀 安装/卸载", "安装/卸载页面 - 功能正常")
    
    def show_model(self):
        self.show_page("🤖 模型管理", "模型管理页面 - 功能正常")
    
    def show_channel(self):
        self.show_page("📱 通道管理", "通道管理页面 - 功能正常")
    
    def show_agent(self):
        self.show_page("👥 Agent管理", "Agent管理页面 - 功能正常")
    
    def show_settings(self):
        self.show_page("⚙️ 设置", "设置页面 - 功能正常")
    
    def show_logs(self):
        self.show_page("📋 日志监控", "日志监控页面 - 功能正常\n状态：监控中 (Monitoring...)")
    
    def show_help(self):
        self.show_page("🆘 帮助", "帮助页面 - 功能正常")
    
    def show_page(self, title, content):
        """显示页面"""
        self.clear_content()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        self.content_layout.addWidget(title_label)
        
        content_label = QLabel(content)
        content_label.setStyleSheet("font-size: 14px;")
        self.content_layout.addWidget(content_label)
        
        self.content_layout.addStretch()


def main():
    """主函数"""
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("码泓mahong-OpenClaw管理器")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("OpenClaw Team")
    
    # 创建主窗口
    window = SimpleMainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()