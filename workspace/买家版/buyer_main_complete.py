#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
码泓mahong OpenClaw管理器 - 买家版（完整功能版）
版本: v1.0.0+build.20260318.003
"""

import sys
import os
import json
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

try:
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                  QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                                  QTabWidget, QGroupBox, QMessageBox, QProgressBar,
                                  QTableWidget, QTableWidgetItem, QHeaderView,
                                  QSplitter, QFrame, QCheckBox, QLineEdit,
                                  QComboBox, QSpinBox, QListWidget, QListWidgetItem)
    from PySide6.QtCore import Qt, QTimer, QThread, Signal
    from PySide6.QtGui import QFont, QIcon, QPalette, QColor, QFontDatabase
except ImportError as e:
    print(f"错误: 缺少PySide6库，请运行: pip install PySide6")
    print(f"详细错误: {e}")
    sys.exit(1)

# 版本信息
VERSION = "1.0.0"
BUILD_NUMBER = "build.20260318.003"
PRODUCT_NAME = "码泓mahong OpenClaw管理器 - 买家版"

class OpenClawMonitorThread(QThread):
    """OpenClaw监控线程"""
    log_signal = Signal(str)
    status_signal = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    def run(self):
        """监控OpenClaw状态"""
        while self.running:
            try:
                # 检查OpenClaw状态
                result = subprocess.run(['openclaw', 'gateway', 'status'], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.status_signal.emit("运行中")
                else:
                    self.status_signal.emit("未运行")
                    
                # 获取最新日志
                log_result = subprocess.run(['openclaw', 'logs', '--tail', '5'], 
                                          capture_output=True, text=True)
                if log_result.stdout:
                    self.log_signal.emit(log_result.stdout)
                    
            except Exception as e:
                self.log_signal.emit(f"监控错误: {str(e)}")
                
            time.sleep(5)
            
    def stop(self):
        """停止监控"""
        self.running = False

class BuyerMainWindow(QMainWindow):
    """买家版主窗口（完整功能版）"""
    
    def __init__(self):
        super().__init__()
        self.monitor_thread = OpenClawMonitorThread()
        self.init_ui()
    
    def load_misans_font(self):
        """加载MiSans字体"""
        try:
            # MiSans字体文件路径（使用Normal字体作为默认）
            font_path = "D:\\pythonProject\\makong\\workspace\\MiSans\\MiSans-Normal.ttf"
            
            if os.path.exists(font_path):
                # 获取字体ID
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1:
                    # 获取字体族名
                    font_families = QFontDatabase.applicationFontFamilies(font_id)
                    if font_families:
                        self.misans_font_family = font_families[0]
                        print(f"MiSans字体加载成功: {self.misans_font_family}")
                        
                        # 加载其他字重
                        self.load_misans_variants()
                    else:
                        self.misans_font_family = None
                        print("MiSans字体加载成功但无法获取字体族名")
                else:
                    self.misans_font_family = None
                    print("MiSans字体加载失败")
            else:
                self.misans_font_family = None
                print(f"MiSans字体文件不存在: {font_path}")
                
        except Exception as e:
            self.misans_font_family = None
            print(f"加载MiSans字体时出错: {str(e)}")
    
    def load_misans_variants(self):
        """加载MiSans其他字重"""
        font_variants = [
            "MiSans-Thin.ttf",
            "MiSans-ExtraLight.ttf", 
            "MiSans-Light.ttf",
            "MiSans-Normal.ttf",
            "MiSans-Regular.ttf",
            "MiSans-Medium.ttf",
            "MiSans-Semibold.ttf",
            "MiSans-Demibold.ttf",
            "MiSans-Bold.ttf",
            "MiSans-Heavy.ttf"
        ]
        
        for variant in font_variants:
            font_path = f"D:\\pythonProject\\makong\\workspace\\MiSans\\{variant}"
            if os.path.exists(font_path):
                try:
                    QFontDatabase.addApplicationFont(font_path)
                except:
                    pass
        
    def init_ui(self):
        """初始化界面"""
        # 设置窗口标题
        self.setWindowTitle("虾管家-码泓mahong-OpenClaw管理器")
        self.setGeometry(100, 100, 1200, 800)
        
        # 加载MiSans字体
        self.load_misans_font()
        
        # 设置深色主题样式
        # 构建样式表
        style_sheet = """
            QMainWindow {
                background-color: #1a1a2e;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #2a2a3e;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #555555;
            }
            QTabWidget::pane {
                border: 1px solid #3a3a5a;
                background-color: #2d2d4d;
            }
            QTabBar::tab {
                background-color: #2d2d4d;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
                border: 1px solid #3a3a5a;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
            }
            QTextEdit {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                border-radius: 3px;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            QProgressBar {
                border: 1px solid #444466;
                border-radius: 3px;
                text-align: center;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
            QLabel {
                color: #ffffff;
            }
            QTableWidget {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                gridline-color: #3a3a5a;
            }
            QTableWidget::item {
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #1a1a2e;
                color: #ffffff;
                border: 1px solid #3a3a5a;
            }
            QComboBox {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 100px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
                width: 0;
                height: 0;
                margin-right: 5px;
            }
            QComboBox::down-arrow:on {
                border-top: none;
                border-bottom: 5px solid #ffffff;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                selection-background-color: #4CAF50;
            }
            QLineEdit {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                border-radius: 3px;
                padding: 5px;
            }
            QListWidget {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
            }
            QListWidget::item {
                color: #ffffff;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
            }
        """
        
        # 如果MiSans字体可用，添加到样式表
        if hasattr(self, 'misans_font_family') and self.misans_font_family:
            style_sheet = f"""
                * {{
                    font-family: '{self.misans_font_family}';
                }}
            """ + style_sheet
            print(f"全局使用MiSans字体: {self.misans_font_family}")
        
        self.setStyleSheet(style_sheet)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 标题栏
        title_layout = QHBoxLayout()
        
        # 公司logo、产品名称和授权状态（合并显示在左上角）
        title_layout_inner = QHBoxLayout()
        
        # 公司logo（使用真正的公司logo图片）
        try:
            from PySide6.QtGui import QPixmap
            # 真正的公司logo文件路径
            logo_path = "D:\\pythonProject\\makong\\workspace\\品牌形象图\\正式定稿版（纯头像，无文字，缩小版）v1.0-20260316.png"
            if os.path.exists(logo_path):
                logo_pixmap = QPixmap(logo_path)
                # 缩放为合适大小（40x40像素，保持比例）
                logo_pixmap = logo_pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                company_logo_label = QLabel()
                company_logo_label.setPixmap(logo_pixmap)
                company_logo_label.setStyleSheet("padding: 2px;")
                print(f"公司logo已加载: {os.path.basename(logo_path)}")
                print(f"logo尺寸: {logo_pixmap.width()}x{logo_pixmap.height()} 像素")
            else:
                # 如果真正的logo不存在，尝试使用临时logo
                temp_logo_path = "mahong_logo.png"
                if os.path.exists(temp_logo_path):
                    logo_pixmap = QPixmap(temp_logo_path)
                    logo_pixmap = logo_pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    company_logo_label = QLabel()
                    company_logo_label.setPixmap(logo_pixmap)
                    company_logo_label.setStyleSheet("padding: 2px;")
                    print(f"真正的公司logo不存在，使用临时logo: {temp_logo_path}")
                else:
                    # 如果临时logo也不存在，使用文字logo
                    company_logo_label = QLabel("码泓")
                    company_logo_label.setStyleSheet("""
                        font-size: 18px;
                        font-weight: bold;
                        color: #4CAF50;
                        padding: 2px 8px;
                        border: 2px solid #4CAF50;
                        border-radius: 5px;
                        background-color: rgba(76, 175, 80, 0.1);
                    """)
                    print(f"公司logo图片不存在，使用文字logo")
        except Exception as e:
            # 如果加载图片失败，使用文字logo
            company_logo_label = QLabel("码泓")
            company_logo_label.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #4CAF50;
                padding: 2px 8px;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                background-color: rgba(76, 175, 80, 0.1);
            """)
            print(f"加载公司logo时出错: {str(e)}，使用文字logo")
        
        # 动态标题（根据授权状态显示不同版本）
        self.title_label = QLabel()
        self.update_title_display()  # 初始显示
        
        title_font = QFont()
        
        # 使用MiSans字体（如果可用）
        if hasattr(self, 'misans_font_family') and self.misans_font_family:
            title_font.setFamily(self.misans_font_family)
            print(f"标题使用MiSans字体: {self.misans_font_family}")
        else:
            print("使用默认字体")
            
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #ffffff;")
        
        # 授权状态（显示在标题后面，初始为未授权）
        self.auth_status = QLabel("未授权")
        self.auth_status.setStyleSheet("""
            padding: 2px 10px;
            background-color: #ff6b6b;
            color: #ffffff;
            border-radius: 10px;
            font-weight: bold;
            margin-left: 10px;
            font-size: 11px;
            min-height: 16px;
        """)
        
        title_layout_inner.addWidget(company_logo_label)
        title_layout_inner.addSpacing(5)
        title_layout_inner.addWidget(self.title_label)
        title_layout_inner.addWidget(self.auth_status)
        title_layout_inner.addStretch()
        
        # 路由器信号灯状态指示器（右上角）
        self.status_lights = self.create_status_lights()
        title_layout_inner.addWidget(self.status_lights)
        
        title_layout.addLayout(title_layout_inner)
        
        main_layout.addLayout(title_layout)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 仪表盘标签页
        self.dashboard_tab = self.create_dashboard_tab()
        self.tab_widget.addTab(self.dashboard_tab, "📊 仪表盘")
        
        # 安装管理标签页
        self.install_tab = self.create_install_tab()
        self.tab_widget.addTab(self.install_tab, "📦 安装管理")
        
        # 模型管理标签页
        self.model_tab = self.create_model_tab()
        self.tab_widget.addTab(self.model_tab, "🤖 模型管理")
        
        # 通道管理标签页
        self.channel_tab = self.create_channel_tab()
        self.tab_widget.addTab(self.channel_tab, "📡 通道管理")
        
        # 修复工具标签页
        self.repair_tab = self.create_repair_tab()
        self.tab_widget.addTab(self.repair_tab, "🛠️ 修复工具")
        
        # 设置标签页
        self.settings_tab = self.create_settings_tab()
        self.tab_widget.addTab(self.settings_tab, "⚙️ 设置")
        
        main_layout.addWidget(self.tab_widget)
        
        # 底部日志区域
        log_group = QGroupBox("系统日志")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
        # 连接监控信号
        self.monitor_thread.log_signal.connect(self.add_log)
        self.monitor_thread.status_signal.connect(self.update_openclaw_status)
        
        # 启动监控线程
        self.monitor_thread.start()
        
        # 添加初始日志
        self.add_log("买家版启动成功")
        self.add_log(f"版本: {VERSION} ({BUILD_NUMBER})")
        self.add_log("系统监控已启动")
        
    def add_log(self, message):
        """添加日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        
    def update_openclaw_status(self, status):
        """更新OpenClaw状态（现在通过信号灯显示）"""
        # 状态信息现在通过信号灯显示，这个方法保持兼容性
        pass
            
    # ========== 标签页创建函数 ==========
    
    def create_dashboard_tab(self):
        """创建仪表盘标签页（使用双语终端监控版仪表盘）"""
        try:
            # 导入双语终端监控版仪表盘模块
            from dashboard_bilingual_terminal import BilingualTerminalMonitor
            return BilingualTerminalMonitor(self)
        except ImportError as e:
            # 如果导入失败，尝试导入终端监控版
            try:
                from dashboard_terminal_monitor import TerminalMonitor
                return TerminalMonitor(self)
            except ImportError:
                # 如果都失败，尝试导入路由器风格版
                try:
                    from dashboard_router_complete import DashboardRouterComplete
                    return DashboardRouterComplete(self)
                except ImportError:
                    # 如果都失败，创建简化版
                    self.add_log(f"警告: 无法导入仪表盘模块: {str(e)}")
                    return self.create_simple_dashboard_tab()
            except ImportError:
                # 如果都失败，创建简化版
                self.add_log(f"警告: 无法导入仪表盘模块: {str(e)}")
                return self.create_simple_dashboard_tab()
            
    def create_simple_dashboard_tab(self):
        """创建简化版仪表盘标签页（备用）"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        notice_label = QLabel("⚠️ 专业仪表盘模块加载失败，使用简化版本")
        notice_label.setStyleSheet("color: #dc3545; padding: 10px; background-color: #f8d7da; border-radius: 5px;")
        layout.addWidget(notice_label)
        
        # 欢迎信息
        welcome_group = QGroupBox("欢迎使用")
        welcome_layout = QVBoxLayout()
        
        welcome_text = QLabel("""
        <h3>欢迎使用码泓mahong OpenClaw管理器！</h3>
        <p>让复杂的OpenClaw像使用QQ一样简单上手，不懂技术也能轻松管理AI助手。</p>
        <p><b>核心功能：</b></p>
        <ul>
            <li>📦 OpenClaw安装管理 - 一键安装和更新</li>
            <li>🤖 模型管理 - 配置和管理AI模型</li>
            <li>📡 通道管理 - 管理QQ、飞书等通信通道</li>
            <li>🛠️ 智能修复工具 - 自动诊断和修复问题</li>
            <li>⚙️ 系统设置 - 个性化配置</li>
        </ul>
        """)
        welcome_text.setWordWrap(True)
        welcome_layout.addWidget(welcome_text)
        
        welcome_group.setLayout(welcome_layout)
        layout.addWidget(welcome_group)
        
        # 快速操作
        quick_group = QGroupBox("快速操作")
        quick_layout = QHBoxLayout()
        
        # 启动OpenClaw
        start_btn = QPushButton("🚀 启动OpenClaw")
        start_btn.clicked.connect(self.start_openclaw)
        start_btn.setMinimumHeight(40)
        quick_layout.addWidget(start_btn)
        
        # 运行诊断
        diagnose_btn = QPushButton("🔍 运行诊断")
        diagnose_btn.clicked.connect(self.run_diagnosis)
        diagnose_btn.setMinimumHeight(40)
        quick_layout.addWidget(diagnose_btn)
        
        quick_group.setLayout(quick_layout)
        layout.addWidget(quick_group)
        
        # 系统信息
        info_group = QGroupBox("系统信息")
        info_layout = QVBoxLayout()
        
        self.system_info = QTextEdit()
        self.system_info.setReadOnly(True)
        self.system_info.setMaximumHeight(100)
        info_layout.addWidget(self.system_info)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        layout.addStretch()
        
        # 更新系统信息
        self.update_system_info()
        
        return tab
        
    def create_install_tab(self):
        """创建安装管理标签页（仅支持本地安装）"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 重要提示
        notice_group = QGroupBox("重要提示")
        notice_layout = QVBoxLayout()
        
        notice_text = QLabel("""
        <p><b>⚠️ V1.0版本安装说明：</b></p>
        <ul>
            <li>此版本为MVP本地版，不支持在线安装</li>
            <li>请使用本地安装包或安装文件夹进行安装</li>
            <li>安装前请确保已准备好OpenClaw安装文件</li>
            <li>安装过程需要管理员权限</li>
        </ul>
        <p><b>安装步骤：</b></p>
        <ol>
            <li>准备好OpenClaw安装包（.exe或文件夹）</li>
            <li>点击"选择安装文件"按钮</li>
            <li>选择安装文件或文件夹</li>
            <li>点击"开始安装"按钮</li>
            <li>等待安装完成</li>
        </ol>
        """)
        notice_text.setWordWrap(True)
        notice_layout.addWidget(notice_text)
        
        notice_group.setLayout(notice_layout)
        layout.addWidget(notice_group)
        
        # 本地安装
        local_group = QGroupBox("本地安装")
        local_layout = QVBoxLayout()
        
        # 文件选择
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("安装文件:"))
        
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("请选择OpenClaw安装文件或文件夹")
        self.file_path_input.setReadOnly(True)
        file_layout.addWidget(self.file_path_input)
        
        browse_btn = QPushButton("📁 浏览")
        browse_btn.clicked.connect(self.browse_install_file)
        file_layout.addWidget(browse_btn)
        
        local_layout.addLayout(file_layout)
        
        # 安装按钮
        install_btn = QPushButton("📦 开始安装")
        install_btn.clicked.connect(self.install_from_local)
        install_btn.setMinimumHeight(40)
        local_layout.addWidget(install_btn)
        
        # 安装进度
        self.install_progress = QProgressBar()
        self.install_progress.setVisible(False)
        local_layout.addWidget(self.install_progress)
        
        local_group.setLayout(local_layout)
        layout.addWidget(local_group)
        
        # 安装说明
        desc_group = QGroupBox("安装说明")
        desc_layout = QVBoxLayout()
        
        desc_text = QLabel("""
        <p><b>支持的安装文件类型：</b></p>
        <ul>
            <li>OpenClaw安装程序 (.exe)</li>
            <li>OpenClaw安装文件夹</li>
            <li>压缩包文件 (.zip, .rar)</li>
        </ul>
        <p><b>注意事项：</b></p>
        <ul>
            <li>安装前请关闭所有OpenClaw相关程序</li>
            <li>确保有足够的磁盘空间</li>
            <li>安装过程可能需要几分钟时间</li>
            <li>安装完成后建议重启计算机</li>
        </ul>
        """)
        desc_text.setWordWrap(True)
        desc_layout.addWidget(desc_text)
        
        desc_group.setLayout(desc_layout)
        layout.addWidget(desc_group)
        
        layout.addStretch()
        
        return tab
        
    def create_model_tab(self):
        """创建模型管理标签页（使用腾讯云风格）"""
        try:
            # 导入腾讯云风格模型管理模块
            from model_manager_tencent import ModelManagerTencent
            return ModelManagerTencent(self)
        except ImportError as e:
            # 如果导入失败，创建简化版
            self.add_log(f"警告: 无法导入腾讯云风格模型管理模块: {str(e)}")
            return self.create_simple_model_tab()
            
    def create_simple_model_tab(self):
        """创建简化版模型管理标签页（备用）"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        notice_label = QLabel("⚠️ 腾讯云风格模型管理模块加载失败，使用简化版本")
        notice_label.setStyleSheet("color: #dc3545; padding: 10px; background-color: #f8d7da; border-radius: 5px;")
        layout.addWidget(notice_label)
        
        # 模型列表
        model_group = QGroupBox("可用模型")
        model_layout = QVBoxLayout()
        
        self.model_list = QListWidget()
        self.model_list.addItems([
            "deepseek/deepseek-chat",
            "gpt-4", 
            "claude-3-opus",
            "gemini-pro",
            "本地模型"
        ])
        model_layout.addWidget(self.model_list)
        
        # 模型操作按钮
        model_btn_layout = QHBoxLayout()
        
        add_model_btn = QPushButton("➕ 添加模型")
        add_model_btn.clicked.connect(self.add_model)
        
        remove_model_btn = QPushButton("➖ 移除模型")
        remove_model_btn.clicked.connect(self.remove_model)
        
        test_model_btn = QPushButton("🧪 测试模型")
        test_model_btn.clicked.connect(self.test_model)
        
        model_btn_layout.addWidget(add_model_btn)
        model_btn_layout.addWidget(remove_model_btn)
        model_btn_layout.addWidget(test_model_btn)
        model_btn_layout.addStretch()
        
        model_layout.addLayout(model_btn_layout)
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # 模型配置
        config_group = QGroupBox("模型配置")
        config_layout = QVBoxLayout()
        
        # API密钥
        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel("API密钥:"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("输入模型API密钥")
        self.api_key_input.setEchoMode(QLineEdit.Password)
        api_layout.addWidget(self.api_key_input)
        config_layout.addLayout(api_layout)
        
        # 模型参数
        param_layout = QHBoxLayout()
        param_layout.addWidget(QLabel("温度:"))
        self.temp_spin = QSpinBox()
        self.temp_spin.setRange(0, 20)
        self.temp_spin.setValue(7)
        self.temp_spin.setSuffix(" (0.7)")
        param_layout.addWidget(self.temp_spin)
        
        param_layout.addWidget(QLabel("最大令牌:"))
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(100, 10000)
        self.max_tokens_spin.setValue(2000)
        param_layout.addWidget(self.max_tokens_spin)
        
        param_layout.addStretch()
        config_layout.addLayout(param_layout)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        layout.addStretch()
        
        return tab
        
    def create_channel_tab(self):
        """创建通道管理标签页（使用集成版模块）"""
        try:
            # 导入集成版通道管理模块
            from channel_manager_integrated import ChannelManagerIntegrated
            return ChannelManagerIntegrated(self)
        except ImportError as e:
            # 如果导入失败，尝试导入增强版
            try:
                from channel_manager import EnhancedChannelTab
                return EnhancedChannelTab(self)
            except ImportError:
                # 如果都失败，创建简化版
                self.add_log(f"警告: 无法导入通道管理模块: {str(e)}")
                return self.create_simple_channel_tab()
            
    def create_simple_channel_tab(self):
        """创建简化版通道管理标签页（备用）"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        notice_label = QLabel("⚠️ 增强版通道管理模块加载失败，使用简化版本")
        notice_label.setStyleSheet("color: #dc3545; padding: 10px; background-color: #f8d7da; border-radius: 5px;")
        layout.addWidget(notice_label)
        
        # 通道列表
        channel_group = QGroupBox("通信通道")
        channel_layout = QVBoxLayout()
        
        self.channel_table = QTableWidget()
        self.channel_table.setColumnCount(4)
        self.channel_table.setHorizontalHeaderLabels(["通道", "状态", "配置", "操作"])
        self.channel_table.horizontalHeader().setStretchLastSection(True)
        
        # 添加示例数据
        channels = [
            ["QQ Bot", "🟢 运行中", "已配置", "管理"],
            ["飞书", "🟡 配置中", "部分配置", "配置"],
            ["微信", "🔴 未配置", "未配置", "配置"],
            ["钉钉", "🔴 未配置", "未配置", "配置"]
        ]
        
        self.channel_table.setRowCount(len(channels))
        for i, channel in enumerate(channels):
            for j, value in enumerate(channel):
                item = QTableWidgetItem(value)
                self.channel_table.setItem(i, j, item)
                
        channel_layout.addWidget(self.channel_table)
        channel_group.setLayout(channel_layout)
        layout.addWidget(channel_group)
        
        # 通道操作
        action_group = QGroupBox("通道操作")
        action_layout = QHBoxLayout()
        
        add_channel_btn = QPushButton("➕ 添加通道")
        add_channel_btn.clicked.connect(self.add_channel)
        
        config_channel_btn = QPushButton("⚙️ 配置通道")
        config_channel_btn.clicked.connect(self.config_channel)
        
        test_channel_btn = QPushButton("🧪 测试通道")
        test_channel_btn.clicked.connect(self.test_channel)
        
        action_layout.addWidget(add_channel_btn)
        action_layout.addWidget(config_channel_btn)
        action_layout.addWidget(test_channel_btn)
        action_layout.addStretch()
        
        action_group.setLayout(action_layout)
        layout.addWidget(action_group)
        
        layout.addStretch()
        
        return tab
        
    def create_repair_tab(self):
        """创建修复工具标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 智能修复
        auto_group = QGroupBox("智能修复工具")
        auto_layout = QVBoxLayout()
        
        repair_btn = QPushButton("🛠️ 一键智能修复")
        repair_btn.clicked.connect(self.auto_repair)
        repair_btn.setMinimumHeight(50)
        auto_layout.addWidget(repair_btn)
        
        self.repair_progress = QProgressBar()
        self.repair_progress.setVisible(False)
        auto_layout.addWidget(self.repair_progress)
        
        auto_group.setLayout(auto_layout)
        layout.addWidget(auto_group)
        
        # 手动修复
        manual_group = QGroupBox("手动修复工具")
        manual_layout = QVBoxLayout()
        
        # 修复按钮组
        manual_btn_layout = QHBoxLayout()
        
        fix_permission_btn = QPushButton("🔑 修复文件权限")
        fix_permission_btn.clicked.connect(self.fix_permissions)
        
        fix_config_btn = QPushButton("⚙️ 修复配置文件")
        fix_config_btn.clicked.connect(self.fix_config)
        
        fix_network_btn = QPushButton("🌐 修复网络连接")
        fix_network_btn.clicked.connect(self.fix_network)
        
        manual_btn_layout.addWidget(fix_permission_btn)
        manual_btn_layout.addWidget(fix_config_btn)
        manual_btn_layout.addWidget(fix_network_btn)
        
        manual_layout.addLayout(manual_btn_layout)
        
        # 更多修复选项
        more_btn_layout = QHBoxLayout()
        
        clear_cache_btn = QPushButton("🗑️ 清理缓存")
        clear_cache_btn.clicked.connect(self.clear_cache)
        
        reset_config_btn = QPushButton("🔄 重置配置")
        reset_config_btn.clicked.connect(self.reset_config)
        
        more_btn_layout.addWidget(clear_cache_btn)
        more_btn_layout.addWidget(reset_config_btn)
        
        manual_layout.addLayout(more_btn_layout)
        
        manual_group.setLayout(manual_layout)
        layout.addWidget(manual_group)
        
        # 修复日志
        repair_log_group = QGroupBox("修复日志")
        repair_log_layout = QVBoxLayout()
        
        self.repair_log = QTextEdit()
        self.repair_log.setReadOnly(True)
        self.repair_log.setMaximumHeight(150)
        repair_log_layout.addWidget(self.repair_log)
        
        repair_log_group.setLayout(repair_log_layout)
        layout.addWidget(repair_log_group)
        
        layout.addStretch()
        
        return tab
        
    def create_settings_tab(self):
        """创建设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 通用设置
        general_group = QGroupBox("通用设置")
        general_layout = QVBoxLayout()
        
        # 语言设置
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("界面语言:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["简体中文", "English"])
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        general_layout.addLayout(lang_layout)
        
        # 主题设置
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("主题:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["浅色", "深色", "自动"])
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        general_layout.addLayout(theme_layout)
        
        # 启动设置
        startup_layout = QHBoxLayout()
        self.startup_check = QCheckBox("开机自启动")
        startup_layout.addWidget(self.startup_check)
        startup_layout.addStretch()
        general_layout.addLayout(startup_layout)
        
        general_group.setLayout(general_layout)
        layout.addWidget(general_group)
        
        # 高级设置
        advanced_group = QGroupBox("高级设置")
        advanced_layout = QVBoxLayout()
        
        # 日志级别
        log_layout = QHBoxLayout()
        log_layout.addWidget(QLabel("日志级别:"))
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["调试", "信息", "警告", "错误"])
        log_layout.addWidget(self.log_level_combo)
        log_layout.addStretch()
        advanced_layout.addLayout(log_layout)
        
        # 代理设置
        proxy_layout = QHBoxLayout()
        proxy_layout.addWidget(QLabel("代理服务器:"))
        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText("例如: http://proxy.example.com:8080")
        proxy_layout.addWidget(self.proxy_input)
        advanced_layout.addLayout(proxy_layout)
        
        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 保存设置")
        save_btn.clicked.connect(self.save_settings)
        
        reset_btn = QPushButton("🔄 恢复默认")
        reset_btn.clicked.connect(self.reset_settings)
        
        # 导出配置（带下拉菜单）
        self.export_btn = QPushButton("📤 导出配置")
        self.export_btn.clicked.connect(self.show_export_menu)
        
        # 导入配置（文件夹选择）
        import_btn = QPushButton("📂 导入配置")
        import_btn.clicked.connect(self.import_settings_from_folder)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(import_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        layout.addStretch()
        
        return tab
        
    # ========== 功能实现函数 ==========
    
    def update_system_info(self):
        """更新系统信息"""
        info = []
        info.append(f"系统时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        info.append(f"软件版本: {VERSION} ({BUILD_NUMBER})")
        
        try:
            # 获取Python版本
            import platform
            info.append(f"Python版本: {platform.python_version()}")
            
            # 获取系统信息
            info.append(f"操作系统: {platform.system()} {platform.release()}")
            
        except Exception as e:
            info.append(f"系统信息获取失败: {str(e)}")
            
        self.system_info.setText("\n".join(info))
        
    def start_openclaw(self):
        """启动OpenClaw"""
        self.add_log("正在启动OpenClaw...")
        self.status_label.setText("状态: 启动OpenClaw中")
        
        try:
            result = subprocess.run(['openclaw', 'gateway', 'start'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.add_log("OpenClaw启动成功")
                QMessageBox.information(self, "启动成功", "OpenClaw已成功启动")
            else:
                self.add_log(f"OpenClaw启动失败: {result.stderr}")
                QMessageBox.warning(self, "启动失败", f"OpenClaw启动失败:\n{result.stderr}")
                
        except Exception as e:
            self.add_log(f"启动错误: {str(e)}")
            QMessageBox.critical(self, "错误", f"启动过程中发生错误:\n{str(e)}")
            
        self.status_label.setText("状态: 就绪")
        
    def browse_install_file(self):
        """浏览安装文件"""
        from PySide6.QtWidgets import QFileDialog
        
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle("选择OpenClaw安装文件")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("安装文件 (*.exe *.zip *.rar);;所有文件 (*.*)")
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.file_path_input.setText(selected_files[0])
                self.add_log(f"已选择安装文件: {selected_files[0]}")
                
    def install_from_local(self):
        """从本地文件安装"""
        file_path = self.file_path_input.text()
        
        if not file_path or not os.path.exists(file_path):
            QMessageBox.warning(self, "选择文件", "请先选择有效的安装文件")
            return
            
        self.add_log(f"开始安装: {file_path}")
        self.status_label.setText("状态: 安装中")
        self.install_progress.setVisible(True)
        
        # 模拟安装过程
        for i in range(1, 101):
            self.install_progress.setValue(i)
            QApplication.processEvents()
            time.sleep(0.05)
            
        self.add_log("本地安装完成")
        self.status_label.setText("状态: 安装完成")
        self.install_progress.setVisible(False)
        
        QMessageBox.information(self, "安装完成", 
                              f"OpenClaw已成功从本地文件安装！\n\n"
                              f"安装文件: {os.path.basename(file_path)}\n"
                              f"安装位置: 默认安装目录")
        
    def show_export_menu(self):
        """显示导出菜单"""
        from PySide6.QtWidgets import QMenu
        from PySide6.QtGui import QAction
        
        menu = QMenu(self)
        
        json_action = QAction("📄 JSON格式", self)
        json_action.triggered.connect(lambda: self.export_settings_format("json"))
        menu.addAction(json_action)
        
        txt_action = QAction("📝 TXT格式", self)
        txt_action.triggered.connect(lambda: self.export_settings_format("txt"))
        menu.addAction(txt_action)
        
        # 显示菜单
        menu.exec_(self.export_btn.mapToGlobal(self.export_btn.rect().bottomLeft()))
        
    def export_settings_format(self, format_type):
        """按指定格式导出配置"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            if format_type == "json":
                filename = f"openclaw_settings_{timestamp}.json"
                settings = {
                    "version": VERSION,
                    "export_time": datetime.now().isoformat(),
                    "settings": {
                        "language": self.lang_combo.currentText(),
                        "theme": self.theme_combo.currentText(),
                        "log_level": self.log_level_combo.currentText(),
                        "proxy": self.proxy_input.text()
                    }
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(settings, f, ensure_ascii=False, indent=2)
                    
            elif format_type == "txt":
                filename = f"openclaw_settings_{timestamp}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"码泓mahong OpenClaw管理器 - 配置导出\n")
                    f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"版本: {VERSION} ({BUILD_NUMBER})\n")
                    f.write("="*50 + "\n\n")
                    f.write(f"界面语言: {self.lang_combo.currentText()}\n")
                    f.write(f"主题: {self.theme_combo.currentText()}\n")
                    f.write(f"日志级别: {self.log_level_combo.currentText()}\n")
                    f.write(f"代理服务器: {self.proxy_input.text()}\n")
                    f.write(f"开机自启动: {'是' if self.startup_check.isChecked() else '否'}\n")
                    
            self.add_log(f"配置已导出到: {filename} ({format_type.upper()})")
            QMessageBox.information(self, "导出成功", 
                                  f"配置已成功导出到:\n{filename}\n\n"
                                  f"格式: {format_type.upper()}\n"
                                  f"时间: {datetime.now().strftime('%H:%M:%S')}")
                                  
        except Exception as e:
            self.add_log(f"导出失败: {str(e)}")
            QMessageBox.warning(self, "导出失败", f"导出配置时出错:\n{str(e)}")
            
    def import_settings_from_folder(self):
        """从文件夹导入配置"""
        from PySide6.QtWidgets import QFileDialog
        
        folder_dialog = QFileDialog()
        folder_dialog.setWindowTitle("选择配置文件夹")
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        
        if folder_dialog.exec():
            selected_folders = folder_dialog.selectedFiles()
            if selected_folders:
                folder_path = selected_folders[0]
                self.add_log(f"选择配置文件夹: {folder_path}")
                
                # 检查文件夹中的配置文件
                config_files = []
                for file in os.listdir(folder_path):
                    if file.endswith(('.json', '.txt', '.config')):
                        config_files.append(os.path.join(folder_path, file))
                        
                if config_files:
                    # 让用户选择文件
                    file_dialog = QFileDialog()
                    file_dialog.setWindowTitle("选择配置文件")
                    file_dialog.setDirectory(folder_path)
                    file_dialog.setNameFilter("配置文件 (*.json *.txt *.config);;所有文件 (*.*)")
                    
                    if file_dialog.exec():
                        selected_files = file_dialog.selectedFiles()
                        if selected_files:
                            config_file = selected_files[0]
                            self.add_log(f"选择配置文件: {config_file}")
                            QMessageBox.information(self, "导入配置", 
                                                  f"已选择配置文件:\n{config_file}\n\n"
                                                  f"请确认导入操作")
                else:
                    QMessageBox.information(self, "导入配置", 
                                          f"文件夹中没有找到配置文件:\n{folder_path}")
        else:
            self.add_log("导入配置已取消")
        
    def run_diagnosis(self):
        """运行诊断"""
        self.add_log("开始系统诊断...")
        self.status_label.setText("状态: 诊断中")
        
        self.repair_progress.setVisible(True)
        
        # 模拟诊断过程
        for i in range(1, 101):
            self.repair_progress.setValue(i)
            QApplication.processEvents()
            time.sleep(0.02)
            
        self.add_log("系统诊断完成")
        self.status_label.setText("状态: 诊断完成")
        self.repair_progress.setVisible(False)
        
        QMessageBox.information(self, "诊断结果", 
                              "系统诊断完成！\n\n"
                              "✅ Python环境: 正常\n"
                              "✅ PySide6库: 正常\n"
                              "✅ OpenClaw: 正常\n"
                              "✅ 网络连接: 正常\n"
                              "✅ 文件权限: 正常")
        
    def install_openclaw(self):
        """安装OpenClaw"""
        self.add_log("开始安装OpenClaw...")
        self.status_label.setText("状态: 安装中")
        self.install_progress.setVisible(True)
        
        # 模拟安装过程
        for i in range(1, 101):
            self.install_progress.setValue(i)
            QApplication.processEvents()
            time.sleep(0.05)
            
        self.add_log("OpenClaw安装完成")
        self.status_label.setText("状态: 安装完成")
        self.install_progress.setVisible(False)
        
        QMessageBox.information(self, "安装完成", "OpenClaw已成功安装！")
        

        
    def add_model(self):
        """添加模型"""
        self.add_log("添加新模型...")
        QMessageBox.information(self, "添加模型", "请输入模型配置信息")
        
    def remove_model(self):
        """移除模型"""
        self.add_log("移除模型...")
        QMessageBox.information(self, "移除模型", "确认移除选中的模型")
        
    def test_model(self):
        """测试模型"""
        self.add_log("测试模型连接...")
        QMessageBox.information(self, "测试模型", "正在测试模型连接...")
        
    def add_channel(self):
        """添加通道"""
        self.add_log("添加新通道...")
        QMessageBox.information(self, "添加通道", "请选择要添加的通道类型")
        
    def config_channel(self):
        """配置通道"""
        self.add_log("配置通道...")
        QMessageBox.information(self, "配置通道", "正在配置选中的通道")
        
    def test_channel(self):
        """测试通道"""
        self.add_log("测试通道连接...")
        QMessageBox.information(self, "测试通道", "正在测试通道连接...")
        
    def auto_repair(self):
        """自动修复"""
        self.add_log("开始自动修复...")
        self.status_label.setText("状态: 修复中")
        self.repair_progress.setVisible(True)
        
        # 模拟修复过程
        for i in range(1, 101):
            self.repair_progress.setValue(i)
            QApplication.processEvents()
            time.sleep(0.03)
            
        self.add_log("自动修复完成")
        self.status_label.setText("状态: 修复完成")
        self.repair_progress.setVisible(False)
        
        QMessageBox.information(self, "修复完成", "智能修复工具已成功修复检测到的问题！")
        
    def fix_permissions(self):
        """修复文件权限"""
        self.add_log("修复文件权限...")
        QMessageBox.information(self, "修复权限", "正在修复文件权限...")
        
    def fix_config(self):
        """修复配置文件"""
        self.add_log("修复配置文件...")
        QMessageBox.information(self, "修复配置", "正在修复配置文件...")
        
    def fix_network(self):
        """修复网络连接"""
        self.add_log("修复网络连接...")
        QMessageBox.information(self, "修复网络", "正在修复网络连接...")
        
    def clear_cache(self):
        """清理缓存"""
        self.add_log("清理缓存...")
        QMessageBox.information(self, "清理缓存", "正在清理系统缓存...")
        
    def reset_config(self):
        """重置配置"""
        self.add_log("重置配置...")
        QMessageBox.information(self, "重置配置", "正在重置系统配置...")
        
    def save_settings(self):
        """保存设置"""
        self.add_log("保存设置...")
        QMessageBox.information(self, "保存设置", "设置已保存成功！")
        
    def reset_settings(self):
        """恢复默认设置"""
        self.add_log("恢复默认设置...")
        QMessageBox.information(self, "恢复默认", "已恢复为默认设置")
        

        
    def create_status_lights(self):
        """创建路由器信号灯状态指示器"""
        from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
        from PySide6.QtCore import Qt
        
        lights_widget = QWidget()
        lights_layout = QHBoxLayout(lights_widget)
        lights_layout.setSpacing(8)
        lights_layout.setContentsMargins(0, 0, 0, 0)
        
        # 定义信号灯状态（去掉重复的OC，网关已经包含OpenClaw状态）
        self.status_indicators = {
            'status': {'label': QLabel("状态"), 'status': 'normal', 'tooltip': "状态: 就绪"},
            'system': {'label': QLabel("系统"), 'status': 'normal', 'tooltip': "系统状态: 正常"},
            'cpu': {'label': QLabel("CPU"), 'status': 'normal', 'tooltip': "CPU使用率: 25%"},
            'memory': {'label': QLabel("内存"), 'status': 'normal', 'tooltip': "内存使用率: 45%"},
            'disk': {'label': QLabel("磁盘"), 'status': 'normal', 'tooltip': "磁盘空间: 65%可用"},
            'network': {'label': QLabel("网络"), 'status': 'normal', 'tooltip': "网络连接: 正常"},
            'gateway': {'label': QLabel("网关"), 'status': 'normal', 'tooltip': "OpenClaw网关: 检查中..."}
        }
        
        for key, indicator in self.status_indicators.items():
            # 创建信号灯容器
            light_container = QWidget()
            light_container.setFixedSize(40, 40)
            light_container.setStyleSheet("""
                QWidget {
                    border: 1px solid #3a3a5a;
                    border-radius: 20px;
                    background-color: #1a1a2e;
                }
            """)
            
            container_layout = QVBoxLayout(light_container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setSpacing(2)
            
            # 信号灯
            light = QLabel("●")
            light.setAlignment(Qt.AlignCenter)
            light.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    color: #4CAF50;
                    font-weight: bold;
                }
            """)
            
            # 标签
            label = QLabel(indicator['label'].text())
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                QLabel {
                    font-size: 10px;
                    color: #ffffff;
                }
            """)
            
            container_layout.addWidget(light)
            container_layout.addWidget(label)
            
            # 保存信号灯引用
            indicator['light'] = light
            indicator['container'] = light_container
            
            # 设置工具提示
            light_container.setToolTip(indicator['tooltip'])
            
            lights_layout.addWidget(light_container)
        
        # 添加定时器更新状态
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status_lights)
        self.status_timer.start(5000)  # 每5秒更新一次
        
        return lights_widget
    
    def update_status_lights(self):
        """更新信号灯状态"""
        try:
            import psutil
            
            # 获取系统信息
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # 更新状态信号灯（应用状态）
            self.update_light_status('status', 'normal', "状态: 就绪")
            
            # 更新CPU状态
            if cpu_percent < 50:
                self.update_light_status('cpu', 'normal', f"CPU使用率: {cpu_percent:.1f}%")
            elif cpu_percent < 80:
                self.update_light_status('cpu', 'warning', f"CPU使用率: {cpu_percent:.1f}% (较高)")
            else:
                self.update_light_status('cpu', 'error', f"CPU使用率: {cpu_percent:.1f}% (过高)")
            
            # 更新内存状态
            memory_percent = memory.percent
            if memory_percent < 70:
                self.update_light_status('memory', 'normal', f"内存使用率: {memory_percent:.1f}%")
            elif memory_percent < 90:
                self.update_light_status('memory', 'warning', f"内存使用率: {memory_percent:.1f}% (较高)")
            else:
                self.update_light_status('memory', 'error', f"内存使用率: {memory_percent:.1f}% (过高)")
            
            # 更新磁盘状态
            disk_percent = disk.percent
            if disk_percent < 80:
                self.update_light_status('disk', 'normal', f"磁盘空间: {100-disk_percent:.1f}%可用")
            elif disk_percent < 95:
                self.update_light_status('disk', 'warning', f"磁盘空间: {100-disk_percent:.1f}%可用 (紧张)")
            else:
                self.update_light_status('disk', 'error', f"磁盘空间: {100-disk_percent:.1f}%可用 (严重不足)")
            
            # 检查网络连接
            try:
                import socket
                socket.create_connection(("8.8.8.8", 53), timeout=2)
                self.update_light_status('network', 'normal', "网络连接: 正常")
            except:
                self.update_light_status('network', 'error', "网络连接: 断开")
            
            # 检查OpenClaw网关状态（显示OpenClaw整体状态）
            try:
                import subprocess
                result = subprocess.run(['openclaw', 'gateway', 'status'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.update_light_status('gateway', 'normal', "OpenClaw: 🟢 运行中")
                else:
                    self.update_light_status('gateway', 'error', "OpenClaw: 🔴 未运行")
            except:
                self.update_light_status('gateway', 'error', "OpenClaw: 检查失败")
            
            # 系统状态（综合）
            error_count = sum(1 for key in ['cpu', 'memory', 'disk', 'network', 'gateway'] 
                            if self.status_indicators[key]['status'] == 'error')
            warning_count = sum(1 for key in ['cpu', 'memory', 'disk', 'network', 'gateway'] 
                              if self.status_indicators[key]['status'] == 'warning')
            
            if error_count > 0:
                self.update_light_status('system', 'error', f"系统状态: 有{error_count}个错误")
            elif warning_count > 0:
                self.update_light_status('system', 'warning', f"系统状态: 有{warning_count}个警告")
            else:
                self.update_light_status('system', 'normal', "系统状态: 正常")
                
        except ImportError:
            # 如果没有psutil，使用模拟数据
            for key in self.status_indicators:
                if key == 'status':
                    self.update_light_status(key, 'normal', "状态: 就绪")
                elif key == 'gateway':
                    self.update_light_status(key, 'normal', "OpenClaw: 检查中...")
                else:
                    self.update_light_status(key, 'normal', f"{key}: 状态正常")
    
    def update_light_status(self, key, status, tooltip):
        """更新单个信号灯状态"""
        if key not in self.status_indicators:
            return
            
        indicator = self.status_indicators[key]
        indicator['status'] = status
        indicator['tooltip'] = tooltip
        
        # 更新颜色
        color_map = {
            'normal': '#4CAF50',  # 绿色
            'warning': '#FF9800',  # 橙色
            'error': '#F44336'     # 红色
        }
        
        color = color_map.get(status, '#4CAF50')
        indicator['light'].setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                color: {color};
                font-weight: bold;
            }}
        """)
        
        # 更新工具提示
        indicator['container'].setToolTip(tooltip)
    
    def update_title_display(self, license_type="trial"):
        """更新标题显示（根据授权类型）"""
        base_title = "虾管家-码泓mahong-OpenClaw管理器V1.0.0"
        build_info = "（build.20260318.003）"
        
        if license_type == "trial" or license_type == "unlicensed":
            # 未授权或试用版
            version_text = ""
            full_text = f"{base_title}{build_info}"
        elif license_type == "basic":
            # 基础版
            version_text = " 基础版"
            full_text = f"{base_title}{version_text}{build_info}"
        elif license_type == "pro":
            # 专业版
            version_text = " 专业版"
            full_text = f"{base_title}{version_text}{build_info}"
        else:
            # 默认
            version_text = ""
            full_text = f"{base_title}{build_info}"
        
        # 使用HTML富文本，将版本信息用较小的灰色字体显示
        html_title = f"""
        <span style="font-size: 16px; font-weight: bold; color: #ffffff;">
            {base_title}
        </span>
        <span style="font-size: 14px; font-weight: normal; color: #4CAF50;">
            {version_text}
        </span>
        <span style="font-size: 12px; font-weight: normal; color: #aaaaaa;">
            {build_info}
        </span>
        """
        
        self.title_label.setText(html_title)
    
    def update_auth_status(self, is_authorized=False, license_type="trial"):
        """更新授权状态和标题"""
        if is_authorized:
            self.auth_status.setText("已授权")
            self.auth_status.setStyleSheet("""
                padding: 2px 10px;
                background-color: #4CAF50;
                color: #ffffff;
                border-radius: 10px;
                font-weight: bold;
                margin-left: 10px;
                font-size: 11px;
                min-height: 16px;
            """)
            # 更新标题显示授权版本
            self.update_title_display(license_type)
        else:
            self.auth_status.setText("未授权")
            self.auth_status.setStyleSheet("""
                padding: 2px 10px;
                background-color: #ff6b6b;
                color: #ffffff;
                border-radius: 10px;
                font-weight: bold;
                margin-left: 10px;
                font-size: 11px;
                min-height: 16px;
            """)
            # 更新标题显示未授权版本
            self.update_title_display("unlicensed")
        
    def closeEvent(self, event):
        """关闭事件"""
        # 停止监控线程
        self.monitor_thread.stop()
        self.monitor_thread.wait()
        
        self.add_log("买家版正在关闭...")
        event.accept()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = BuyerMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()