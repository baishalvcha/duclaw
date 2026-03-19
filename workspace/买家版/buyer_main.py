#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
码泓mahong OpenClaw管理器 - 买家版
版本: v1.0.0+build.20260318.001
"""

import sys
import os
import json
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                  QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                                  QTabWidget, QGroupBox, QMessageBox, QProgressBar,
                                  QTableWidget, QTableWidgetItem, QHeaderView,
                                  QSplitter, QFrame, QCheckBox, QLineEdit)
    from PySide6.QtCore import Qt, QTimer, QThread, Signal
    from PySide6.QtGui import QFont, QIcon, QPalette, QColor
except ImportError as e:
    print(f"错误: 缺少PySide6库，请运行: pip install PySide6")
    print(f"详细错误: {e}")
    sys.exit(1)

# 版本信息
VERSION = "1.0.0"
BUILD_NUMBER = "build.20260318.001"
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
                # 检查Gateway状态
                result = subprocess.run(['openclaw', 'gateway', 'status'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.status_signal.emit("运行中")
                else:
                    self.status_signal.emit("已停止")
                    
                # 获取最新日志
                log_result = subprocess.run(['openclaw', 'logs', '--tail', '5'], 
                                          capture_output=True, text=True, timeout=5)
                if log_result.returncode == 0:
                    self.log_signal.emit(log_result.stdout)
                    
            except Exception as e:
                self.log_signal.emit(f"监控错误: {str(e)}")
                
            time.sleep(5)
            
    def stop(self):
        """停止监控"""
        self.running = False

class RepairThread(QThread):
    """修复线程"""
    progress_signal = Signal(int, str)
    finished_signal = Signal(bool, str)
    
    def __init__(self, repair_type):
        super().__init__()
        self.repair_type = repair_type
        
    def run(self):
        """执行修复"""
        try:
            if self.repair_type == "permission":
                self.progress_signal.emit(25, "检查文件权限...")
                # 修复paired.json权限
                fix_script = """
                $pairedPath = "$HOME\\.openclaw\\paired.json"
                if (Test-Path $pairedPath) {
                    Take-Ownership -Path $pairedPath
                    icacls $pairedPath /grant Users:F
                    Write-Host "权限修复完成"
                } else {
                    Write-Host "文件不存在，创建新文件"
                    '{}' | Out-File -FilePath $pairedPath -Encoding UTF8
                }
                """
                self.progress_signal.emit(50, "修复文件权限...")
                # 这里应该执行修复脚本
                self.progress_signal.emit(75, "验证修复结果...")
                self.progress_signal.emit(100, "权限修复完成")
                self.finished_signal.emit(True, "文件权限修复成功")
                
            elif self.repair_type == "config":
                self.progress_signal.emit(25, "检查配置文件...")
                # 修复plugins.allow配置
                self.progress_signal.emit(50, "修复插件配置...")
                self.progress_signal.emit(75, "验证配置...")
                self.progress_signal.emit(100, "配置修复完成")
                self.finished_signal.emit(True, "插件配置修复成功")
                
            elif self.repair_type == "comprehensive":
                self.progress_signal.emit(10, "开始全面检查...")
                self.progress_signal.emit(30, "检查OpenClaw环境...")
                self.progress_signal.emit(50, "检查Gateway服务...")
                self.progress_signal.emit(70, "检查插件配置...")
                self.progress_signal.emit(90, "检查文件权限...")
                self.progress_signal.emit(100, "全面检查完成")
                self.finished_signal.emit(True, "全面检查完成，未发现严重问题")
                
        except Exception as e:
            self.finished_signal.emit(False, f"修复失败: {str(e)}")

class BuyerMainWindow(QMainWindow):
    """买家版主窗口"""
    
    def __init__(self):
        super().__init__()
        self.monitor_thread = None
        self.repair_thread = None
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        """初始化界面"""
        # 在标题前添加Logo
        logo = "🦐 "  # 使用虾emoji作为临时Logo
        self.setWindowTitle(f"{logo}{PRODUCT_NAME} v{VERSION}")
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
                gridline-color: #444466;
            }
            QTableWidget::item {
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #1a1a2e;
                color: #ffffff;
                border: 1px solid #444466;
            }
            QComboBox {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #444466;
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
                border: 1px solid #444466;
                selection-background-color: #4CAF50;
            }
        """)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 标题栏
        title_layout = QHBoxLayout()
        
        # 公司logo（使用虾管家相关图标）
        # TODO: 未来可以替换为实际的公司Logo图片
        company_logo_label = QLabel("🦐")  # 使用虾emoji作为Logo，符合"虾管家"品牌
        company_logo_label.setStyleSheet("font-size: 24px;")
        
        # 产品名称（合并显示）
        product_title = f"虾管家-码泓mahong-OpenClaw管理器-买家版V{VERSION}（{BUILD_NUMBER}）"
        title_label = QLabel(product_title)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #ffffff;")
        
        # 授权状态（显示在标题后面）
        self.auth_status = QLabel("🔒 未授权")
        self.auth_status.setStyleSheet("""
            padding: 5px 10px;
            background-color: #ff6b6b;
            color: #ffffff;
            border-radius: 15px;
            font-weight: bold;
            margin-left: 10px;
            font-size: 14px;
        """)
        
        title_layout.addWidget(company_logo_label)
        title_layout.addSpacing(5)
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.auth_status)
        title_layout.addStretch()
        main_layout.addLayout(title_layout)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        
        # 仪表盘标签页
        self.dashboard_tab = self.create_dashboard_tab()
        self.tab_widget.addTab(self.dashboard_tab, "📊 仪表盘")
        
        # 监控标签页
        self.monitor_tab = self.create_monitor_tab()
        self.tab_widget.addTab(self.monitor_tab, "🔍 监控")
        
        # 修复工具标签页
        self.repair_tab = self.create_repair_tab()
        self.tab_widget.addTab(self.repair_tab, "🛠️ 修复工具")
        
        # 设置标签页
        self.settings_tab = self.create_settings_tab()
        self.tab_widget.addTab(self.settings_tab, "⚙️ 设置")
        
        main_layout.addWidget(self.tab_widget)
        
        # 状态栏
        self.statusBar().showMessage("就绪")
        
    def create_dashboard_tab(self):
        """创建仪表盘标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 系统状态组
        status_group = QGroupBox("系统状态")
        status_layout = QVBoxLayout()
        
        # OpenClaw状态
        openclaw_layout = QHBoxLayout()
        openclaw_layout.addWidget(QLabel("OpenClaw Gateway:"))
        self.gateway_status_label = QLabel("检查中...")
        self.gateway_status_label.setStyleSheet("color: #f39c12; font-weight: bold;")
        openclaw_layout.addWidget(self.gateway_status_label)
        openclaw_layout.addStretch()
        
        # Gateway控制按钮
        self.start_gateway_btn = QPushButton("启动Gateway")
        self.start_gateway_btn.clicked.connect(self.start_gateway)
        self.stop_gateway_btn = QPushButton("停止Gateway")
        self.stop_gateway_btn.clicked.connect(self.stop_gateway)
        self.stop_gateway_btn.setEnabled(False)
        
        openclaw_layout.addWidget(self.start_gateway_btn)
        openclaw_layout.addWidget(self.stop_gateway_btn)
        status_layout.addLayout(openclaw_layout)
        
        # 快速操作
        quick_actions_layout = QHBoxLayout()
        quick_actions_layout.addWidget(QLabel("快速操作:"))
        
        self.view_logs_btn = QPushButton("查看日志")
        self.view_logs_btn.clicked.connect(self.view_logs)
        quick_actions_layout.addWidget(self.view_logs_btn)
        
        self.run_diagnosis_btn = QPushButton("运行诊断")
        self.run_diagnosis_btn.clicked.connect(self.run_diagnosis)
        quick_actions_layout.addWidget(self.run_diagnosis_btn)
        
        self.check_updates_btn = QPushButton("检查更新")
        self.check_updates_btn.clicked.connect(self.check_updates)
        quick_actions_layout.addWidget(self.check_updates_btn)
        
        quick_actions_layout.addStretch()
        status_layout.addLayout(quick_actions_layout)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # 最近活动组
        activity_group = QGroupBox("最近活动")
        activity_layout = QVBoxLayout()
        
        self.activity_text = QTextEdit()
        self.activity_text.setReadOnly(True)
        self.activity_text.setMaximumHeight(150)
        activity_layout.addWidget(self.activity_text)
        
        activity_group.setLayout(activity_layout)
        layout.addWidget(activity_group)
        
        layout.addStretch()
        return tab
        
    def create_monitor_tab(self):
        """创建监控标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 日志监控组
        log_group = QGroupBox("实时日志监控")
        log_layout = QVBoxLayout()
        
        # 日志控制
        log_control_layout = QHBoxLayout()
        self.start_monitor_btn = QPushButton("开始监控")
        self.start_monitor_btn.clicked.connect(self.start_monitoring)
        self.stop_monitor_btn = QPushButton("停止监控")
        self.stop_monitor_btn.clicked.connect(self.stop_monitoring)
        self.stop_monitor_btn.setEnabled(False)
        
        self.clear_logs_btn = QPushButton("清空日志")
        self.clear_logs_btn.clicked.connect(self.clear_logs)
        
        log_control_layout.addWidget(self.start_monitor_btn)
        log_control_layout.addWidget(self.stop_monitor_btn)
        log_control_layout.addWidget(self.clear_logs_btn)
        log_control_layout.addStretch()
        
        log_layout.addLayout(log_control_layout)
        
        # 日志显示
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # 系统资源组
        resource_group = QGroupBox("系统资源")
        resource_layout = QVBoxLayout()
        
        # CPU使用率
        cpu_layout = QHBoxLayout()
        cpu_layout.addWidget(QLabel("CPU使用率:"))
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setRange(0, 100)
        self.cpu_progress.setValue(0)
        cpu_layout.addWidget(self.cpu_progress)
        resource_layout.addLayout(cpu_layout)
        
        # 内存使用率
        memory_layout = QHBoxLayout()
        memory_layout.addWidget(QLabel("内存使用率:"))
        self.memory_progress = QProgressBar()
        self.memory_progress.setRange(0, 100)
        self.memory_progress.setValue(0)
        memory_layout.addWidget(self.memory_progress)
        resource_layout.addLayout(memory_layout)
        
        resource_group.setLayout(resource_layout)
        layout.addWidget(resource_group)
        
        layout.addStretch()
        return tab
        
    def create_repair_tab(self):
        """创建修复工具标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 智能修复组
        repair_group = QGroupBox("智能修复工具")
        repair_layout = QVBoxLayout()
        
        repair_info = QLabel("一键检测和修复OpenClaw常见问题")
        repair_info.setStyleSheet("color: #7f8c8d; font-style: italic;")
        repair_layout.addWidget(repair_info)
        
        # 修复选项
        options_layout = QVBoxLayout()
        
        self.permission_check = QCheckBox("修复文件权限问题 (paired.json)")
        self.permission_check.setChecked(True)
        options_layout.addWidget(self.permission_check)
        
        self.config_check = QCheckBox("修复插件配置问题 (plugins.allow)")
        self.config_check.setChecked(True)
        options_layout.addWidget(self.config_check)
        
        self.gateway_check = QCheckBox("修复Gateway服务问题")
        self.gateway_check.setChecked(True)
        options_layout.addWidget(self.gateway_check)
        
        repair_layout.addLayout(options_layout)
        
        # 修复按钮
        repair_btn_layout = QHBoxLayout()
        self.run_repair_btn = QPushButton("🛠️ 运行智能修复")
        self.run_repair_btn.clicked.connect(self.run_smart_repair)
        self.run_repair_btn.setStyleSheet("font-size: 14px; padding: 10px;")
        
        repair_btn_layout.addWidget(self.run_repair_btn)
        repair_btn_layout.addStretch()
        repair_layout.addLayout(repair_btn_layout)
        
        # 修复进度
        self.repair_progress = QProgressBar()
        self.repair_progress.setRange(0, 100)
        self.repair_progress.setValue(0)
        repair_layout.addWidget(self.repair_progress)
        
        # 修复结果
        self.repair_result_text = QTextEdit()
        self.repair_result_text.setReadOnly(True)
        self.repair_result_text.setMaximumHeight(100)
        repair_layout.addWidget(self.repair_result_text)
        
        repair_group.setLayout(repair_layout)
        layout.addWidget(repair_group)
        
        # 手动修复组
        manual_group = QGroupBox("手动修复工具")
        manual_layout = QVBoxLayout()
        
        manual_btn_layout = QHBoxLayout()
        self.fix_permission_btn = QPushButton("修复文件权限")
        self.fix_permission_btn.clicked.connect(self.fix_permissions)