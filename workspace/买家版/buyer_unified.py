#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一买家版入口
根据授权码确定版本（基础版、专业版）
单一文件发布，动态功能控制
"""

import sys
import os
from datetime import datetime

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QPushButton, QTabWidget, 
                               QGroupBox, QTextEdit, QLineEdit, QMessageBox,
                               QProgressBar, QTableWidget, QTableWidgetItem,
                               QListWidget, QListWidgetItem, QComboBox)
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtGui import QFont, QIcon

# 导入授权管理模块
try:
    from auth_manager import get_auth_manager
    from feature_gate import get_feature_gate
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from auth_manager import get_auth_manager
    from feature_gate import get_feature_gate

# 产品信息
PRODUCT_NAME = "虾管家-码泓mahong-OpenClaw管理器"
VERSION = "1.0.0"
BUILD_NUMBER = "build.20260318.003"


class SystemMonitorThread(QThread):
    """系统监控线程"""
    log_signal = Signal(str)
    status_signal = Signal(str)
    
    def run(self):
        """线程运行"""
        import time
        import psutil
        
        while True:
            # 模拟系统状态检查
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log_signal.emit(f"系统状态更新: {current_time}")
            
            # 检查OpenClaw状态
            openclaw_running = self._check_openclaw_running()
            if openclaw_running:
                self.status_signal.emit("运行中")
            else:
                self.status_signal.emit("未运行")
            
            time.sleep(5)
    
    def _check_openclaw_running(self):
        """检查OpenClaw是否运行"""
        try:
            import psutil
            for proc in psutil.process_iter(['name']):
                if 'openclaw' in proc.info['name'].lower():
                    return True
            return False
        except:
            return False


class BuyerUnifiedWindow(QMainWindow):
    """统一买家版主窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化授权管理器
        self.auth_manager = get_auth_manager()
        self.feature_gate = get_feature_gate()
        
        # 初始化UI
        self.init_ui()
        
        # 启动系统监控
        self.monitor_thread = SystemMonitorThread()
        self.monitor_thread.log_signal.connect(self.add_log)
        self.monitor_thread.status_signal.connect(self.update_openclaw_status)
        self.monitor_thread.start()
        
        # 添加初始日志
        self.add_log("统一买家版启动成功")
        self.add_log(f"版本: {VERSION} ({BUILD_NUMBER})")
        self.add_log(f"授权类型: {self.auth_manager.get_license_name()}")
        self.add_log("系统监控已启动")
    
    def init_ui(self):
        """初始化界面"""
        # 设置窗口标题
        self.setWindowTitle(f"{PRODUCT_NAME} v{VERSION}")
        self.setGeometry(100, 100, 1200, 800)
        
        # 设置深色主题样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a2e;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #2d2d4d;
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
                color: #aaaaaa;
            }
            QTextEdit {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #444466;
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
                border: 1px solid #444466;
            }
            QTableWidget::item {
                color: #ffffff;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50;
            }
            QHeaderView::section {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #444466;
                padding: 5px;
            }
            QListWidget {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #444466;
            }
            QListWidget::item {
                color: #ffffff;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
            }
            QLineEdit {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #444466;
                border-radius: 3px;
                padding: 5px;
            }
            QComboBox {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #444466;
                border-radius: 3px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #444466;
            }
        """)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 标题栏
        title_layout = QHBoxLayout()
        
        # 公司logo、产品名称和授权状态
        title_inner_layout = QHBoxLayout()
        
        # 公司logo
        company_logo_label = QLabel("🦐")  # 使用虾emoji作为Logo
        company_logo_label.setStyleSheet("font-size: 24px;")
        
        # 产品名称和版本号
        license_name = self.auth_manager.get_license_name()
        product_title = f"{PRODUCT_NAME}-{license_name}版 V{VERSION}（{BUILD_NUMBER}）"
        title_label = QLabel(product_title)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #ffffff;")
        
        # 授权状态
        auth_status_text = self._get_auth_status_text()
        self.auth_status_label = QLabel(auth_status_text)
        self.auth_status_label.setStyleSheet(self._get_auth_status_style())
        
        title_inner_layout.addWidget(company_logo_label)
        title_inner_layout.addSpacing(5)
        title_inner_layout.addWidget(title_label)
        title_inner_layout.addWidget(self.auth_status_label)
        title_inner_layout.addStretch()
        
        title_layout.addLayout(title_inner_layout)
        main_layout.addLayout(title_layout)
        
        # 状态栏
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("状态: 就绪")
        self.status_label.setStyleSheet("""
            padding: 5px;
            background-color: #ecf0f1;
            color: #333333;
            border-radius: 3px;
            font-weight: bold;
        """)
        
        self.openclaw_status = QLabel("OpenClaw: 检查中...")
        self.openclaw_status.setStyleSheet("""
            padding: 5px;
            background-color: #ecf0f1;
            color: #333333;
            border-radius: 3px;
            font-weight: bold;
        """)
        
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.openclaw_status)
        
        main_layout.addLayout(status_layout)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 仪表盘标签页
        self.dashboard_tab = self.create_dashboard_tab()
        self.tab_widget.addTab(self.dashboard_tab, "📊 仪表盘")
        
        # 安装管理标签页
        self.install_tab = self.create_install_tab()
        self.tab_widget.addTab(self.install_tab, "📦 安装管理")
        
        # 授权管理标签页
        self.auth_tab = self.create_auth_tab()
        self.tab_widget.addTab(self.auth_tab, "🔑 授权管理")
        
        # 根据授权类型动态添加标签页
        if self.feature_gate.is_enabled("model_management"):
            self.model_tab = self.create_model_tab()
            self.tab_widget.addTab(self.model_tab, "🤖 模型管理")
        
        if self.feature_gate.is_enabled("channel_management"):
            self.channel_tab = self.create_channel_tab()
            self.tab_widget.addTab(self.channel_tab, "📡 通道管理")
        
        if self.feature_gate.is_enabled("batch_operations"):
            self.batch_tab = self.create_batch_tab()
            self.tab_widget.addTab(self.batch_tab, "⚡ 批量操作")
        
        if self.feature_gate.is_enabled("performance_dashboard"):
            self.performance_tab = self.create_performance_tab()
            self.tab_widget.addTab(self.performance_tab, "📈 性能分析")
        
        # 修复工具标签页（所有版本都有）
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
    
    def _get_auth_status_text(self):
        """获取授权状态文本"""
        if self.auth_manager.is_activated():
            license_type = self.auth_manager.get_license_type()
            if license_type == "trial":
                remaining = self.auth_manager.get_remaining_days()
                if remaining is not None:
                    return f"✅ 试用版（剩余{remaining}天）"
                else:
                    return "✅ 试用版"
            elif license_type == "basic":
                return "✅ 基础版"
            elif license_type == "pro":
                return "✅ 专业版"
            else:
                return "✅ 已授权"
        else:
            return "🔒 未授权"
    
    def _get_auth_status_style(self):
        """获取授权状态样式"""
        if self.auth_manager.is_activated():
            license_type = self.auth_manager.get_license_type()
            if license_type == "trial":
                return """
                    padding: 5px 10px;
                    background-color: #FF9800;
                    color: #ffffff;
                    border-radius: 15px;
                    font-weight: bold;
                    margin-left: 10px;
                    font-size: 14px;
                """
            elif license_type == "basic":
                return """
                    padding: 5px 10px;
                    background-color: #2196F3;
                    color: #ffffff;
                    border-radius: 15px;
                    font-weight: bold;
                    margin-left: 10px;
                    font-size: 14px;
                """
            elif license_type == "pro":
                return """
                    padding: 5px 10px;
                    background-color: #4CAF50;
                    color: #ffffff;
                    border-radius: 15px;
                    font-weight: bold;
                    margin-left: 10px;
                    font-size: 14px;
                """
            else:
                return """
                    padding: 5px 10px;
                    background-color: #4CAF50;
                    color: #ffffff;
                    border-radius: 15px;
                    font-weight: bold;
                    margin-left: 10px;
                    font-size: 14px;
                """
        else:
            return """
                padding: 5px 10px;
                background-color: #ff6b6b;
                color: #ffffff;
                border-radius: 15px;
                font-weight: bold;
                margin-left: 10px;
                font-size: 14px;
            """
    
    def create_dashboard_tab(self):
        """创建仪表盘标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 系统状态组
        status_group = QGroupBox("系统状态")
        status_layout = QVBoxLayout()
        
        # CPU使用率
        cpu_layout = QHBoxLayout()
        cpu_label = QLabel("CPU使用率:")
        cpu_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setRange(0, 100)
        self.cpu_progress.setValue(0)
        
        cpu_layout.addWidget(cpu_label)
        cpu_layout.addWidget(self.cpu_progress)
        status_layout.addLayout(cpu_layout)
        
        # 内存使用率
        memory_layout = QHBoxLayout()
        memory_label = QLabel("内存使用率:")
        memory_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        self.memory_progress = QProgressBar()
        self.memory_progress.setRange(0, 100)
        self.memory_progress.setValue(0)
        
        memory_layout.addWidget(memory_label)
        memory_layout.addWidget(self.memory_progress)
        status_layout.addLayout(memory_layout)
        
        # 磁盘使用率
        disk_layout = QHBoxLayout()
        disk_label = QLabel("磁盘使用率:")
        disk_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        self.disk_progress = QProgressBar()
        self.disk_progress.setRange(0, 100)
        self.disk_progress.setValue(0)
        
        disk_layout.addWidget(disk_label)
        disk_layout.addWidget(self.disk_progress)
        status_layout.addLayout(disk_layout)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # 启动系统资源监控
        self._start_resource_monitoring()
        
        layout.addStretch()
        return tab
    
    def create_install_tab(self):
        """创建安装管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 安装OpenClaw
        install_group = QGroupBox("安装OpenClaw")
        install_layout = QVBoxLayout()
        
        install_btn = QPushButton("一键安装OpenClaw")
        install_btn.clicked.connect(self.install_openclaw)
        install_layout.addWidget(install_btn)
        
        # 检查安装状态
        check_btn = QPushButton("检查安装状态")
        check_btn.clicked.connect(self.check_installation)
        install_layout.addWidget(check_btn)
        
        install_group.setLayout(install_layout)
        layout.addWidget(install_group)
        
        # 更新管理
        update_group = QGroupBox("更新管理")
        update_layout = QVBoxLayout()
        
        check_update_btn = QPushButton("检查更新")
        check_update_btn.clicked.connect(self.check_for_updates)
        update_layout.addWidget(check_update_btn)
        
        # 根据授权类型控制更新按钮
        if self.feature_gate.is_enabled("update_openclaw"):
            update_btn = QPushButton("更新OpenClaw")
            update_btn.clicked.connect(self.update_openclaw)
            update_layout.addWidget(update_btn)
        else:
            update_label = QLabel("⚠️ 更新功能需要专业版授权")
            update_label.setStyleSheet("color: #FF9800; font-weight: bold; padding: 10px;")
            update_layout.addWidget(update_label)
        
        update_group.setLayout(update_layout)
        layout.addWidget(update_group)
        
        layout.addStretch()
        return tab
    
    def create_auth_tab(self):
        """创建授权管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 当前授权状态
        current_auth_group = QGroupBox("当前授权状态")
        current_auth_layout = QVBoxLayout()
        
        # 授权类型
        auth_type_layout = QHBoxLayout()
        auth_type_label = QLabel("授权类型:")
        auth_type_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        self.auth_type_value = QLabel(self.auth_manager.get_license_name())
        self.auth_type_value.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 16px;")
        
        auth_type_layout.addWidget(auth_type_label)
        auth_type_layout.addStretch()
        auth_type_layout.addWidget(self.auth_type_value)
        current_auth_layout.addLayout(auth_type_layout)
        
        # 授权状态
        auth_status_layout = QHBoxLayout()
        auth_status_label = QLabel("授权状态:")
        auth_status_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        auth_status_text = "已激活" if self.auth_manager.is_activated() else "未激活"
        self.auth_status_value = QLabel(auth_status_text)
        self.auth_status_value.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 16px;" if self.auth_manager.is_activated() else "color: #ff6b6b; font-weight: bold; font-size: 16px;")
        
        auth_status_layout.addWidget(auth_status_label)
        auth_status_layout.addStretch()
        auth_status_layout.addWidget(self.auth_status_value)
        current_auth_layout.addLayout(auth_status_layout)
        
        # 激活日期
        if self.auth_manager.is_activated():
            activation_date = self.auth_manager.get_current_license_info().get("activation_date")
            if activation_date:
                activation_layout = QHBoxLayout()
                activation_label = QLabel("激活日期:")
                activation_label.setStyleSheet("color: #ffffff; font-weight: bold;")
                activation_value = QLabel(activation_date[:10])  # 只显示日期
                activation_value.setStyleSheet("color: #ffffff;")
                
                activation_layout.addWidget(activation_label)
                activation_layout.addStretch()
                activation_layout.addWidget(activation_value)
                current_auth_layout.addLayout(activation_layout)
        
        # 剩余天数（试用版）
        if self.auth_manager.get_license_type() == "trial":
            remaining_days = self.auth_manager.get_remaining_days()
            if remaining_days is not None:
                remaining_layout = QHBoxLayout()
                remaining_label = QLabel("剩余天数:")
                remaining_label.setStyleSheet("color: #ffffff; font-weight: bold;")
                remaining_value = QLabel(str(remaining_days))
                remaining_value.setStyleSheet("color: #FF9800; font-weight: bold; font-size: 16px;")
                
                remaining_layout.addWidget(remaining_label)
                remaining_layout.addStretch()
                remaining_layout.addWidget(remaining_value)
                current_auth_layout.addLayout(remaining_layout)
        
        current_auth_group.setLayout(current_auth_layout)
        layout.addWidget(current_auth_group)
        
        # 激活授权
        activate_group = QGroupBox("激活授权")
        activate_layout = QVBoxLayout()
        
        # 授权码输入
        license_layout = QHBoxLayout()
        license_label = QLabel("授权码:")
        license_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("请输入您的授权码")
        
        license_layout.addWidget(license_label)
        license_layout.addWidget(self.license_input)
        activate_layout.addLayout(license_layout)
        
        # 激活按钮
        activate_btn = QPushButton("激活授权")
        activate_btn.clicked.connect(self.activate_license)
        activate_layout.addWidget(activate_btn)
        
        # 测试授权码提示
        test_hint = QLabel("测试授权码: TEST-BASIC-1234 (基础版), TEST-PRO-1234 (专业版)")
        test_hint.setStyleSheet("color: #a0a0c0; font-size: 12px; padding: 5px;")
        activate_layout.addWidget(test_hint)
        
        activate_group.setLayout(activate_layout)
        layout.addWidget(activate_group)
        
        # 功能对比
        feature_group = QGroupBox("版本功能对比")
        feature_layout = QVBoxLayout()
        
        # 获取功能摘要
        feature_summary = self.feature_gate.get_license_summary()
        
        # 显示功能统计
        stats_layout = QHBoxLayout()
        total_label = QLabel(f"总功能数: {feature_summary['total_features']}")
        enabled_label = QLabel(f"可用功能: {feature_summary['enabled_features']}")
        disabled_label = QLabel(f"受限功能: {feature_summary['disabled_features']}")
        
        total_label.setStyleSheet("color: #ffffff; padding: 5px;")
        enabled_label.setStyleSheet("color: #4CAF50; padding: 5px;")
        disabled_label.setStyleSheet("color: #ff6b6b; padding: 5px;")
        
        stats_layout.addWidget(total_label)
        stats_layout.addWidget(enabled_label)
        stats_layout.addWidget(disabled_label)
        feature_layout.addLayout(stats_layout)
        
        # 升级提示
        if self.auth_manager.get_license_type() in ["trial", "basic"]:
            upgrade_label = QLabel("💡 升级到专业版可解锁所有高级功能")
            upgrade_label.setStyleSheet("color: #FF9800; font-weight: bold; padding: 10px; background-color: #2d2d4d; border-radius: 5px;")
            feature_layout.addWidget(upgrade_label)
        
        feature_group.setLayout(feature_layout)
        layout.addWidget(feature_group)
        
        layout.addStretch()
        return tab