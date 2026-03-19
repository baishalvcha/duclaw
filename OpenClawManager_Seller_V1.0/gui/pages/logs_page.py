#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志监控窗口
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QLineEdit, QComboBox, QGroupBox, QCheckBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QTextCharFormat, QColor

from gui.language import language_manager
from integration.cli_integration import CLIIntegration


class LogsPage(QWidget):
    """日志监控窗口"""
    
    def __init__(self):
        super().__init__()
        self.cli_integration = CLIIntegration()
        self.is_logging = False
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("日志监控 (Logs)")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # 控制面板
        control_group = QGroupBox("控制面板 (Control Panel)")
        control_layout = QHBoxLayout(control_group)
        
        # 开始/停止按钮
        self.start_stop_btn = QPushButton("开始监控 (Start Monitoring)")
        self.start_stop_btn.clicked.connect(self.toggle_logging)
        control_layout.addWidget(self.start_stop_btn)
        
        # 清除按钮
        clear_btn = QPushButton("清除日志 (Clear Logs)")
        clear_btn.clicked.connect(self.clear_logs)
        control_layout.addWidget(clear_btn)
        
        layout.addWidget(control_group)
        
        # 过滤和搜索
        filter_group = QGroupBox("过滤和搜索 (Filter & Search)")
        filter_layout = QVBoxLayout(filter_group)
        
        # 日志级别过滤
        level_layout = QHBoxLayout()
        level_label = QLabel("日志级别:")
        level_label.setToolTip("Log Level")
        self.level_combo = QComboBox()
        self.level_combo.addItems(["全部 (All)", "INFO", "WARN", "ERROR", "DEBUG"])
        level_layout.addWidget(level_label)
        level_layout.addWidget(self.level_combo)
        level_layout.addStretch()
        
        # 搜索框
        search_layout = QHBoxLayout()
        search_label = QLabel("搜索:")
        search_label.setToolTip("Search")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入关键词 (Enter keywords)")
        self.search_edit.textChanged.connect(self.filter_logs)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        
        filter_layout.addLayout(level_layout)
        filter_layout.addLayout(search_layout)
        
        layout.addWidget(filter_group)
        
        # 日志显示
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("font-family: Consolas, Monaco, monospace; font-size: 10pt;")
        layout.addWidget(self.log_text)
        
        # 状态栏
        status_layout = QHBoxLayout()
        self.status_label = QLabel("未监控 (Not Monitoring)")
        self.status_label.setStyleSheet("color: #666;")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        
        layout.addLayout(status_layout)
    
    def toggle_logging(self):
        """切换日志监控状态"""
        if not self.is_logging:
            # 开始监控
            self.start_logging()
        else:
            # 停止监控
            self.stop_logging()
    
    def start_logging(self):
        """开始日志监控"""
        self.is_logging = True
        self.start_stop_btn.setText("停止监控 (Stop Monitoring)")
        self.status_label.setText("监控中 (Monitoring...)")
        self.status_label.setStyleSheet("color: #28a745;")
        
        # 异步执行日志命令
        def output_callback(line):
            self.add_log(line)
        
        def error_callback(error):
            self.add_log(f"ERROR: {error}", "ERROR")
        
        def done_callback(returncode):
            self.is_logging = False
            self.start_stop_btn.setText("开始监控 (Start Monitoring)")
            self.status_label.setText("监控已停止 (Monitoring Stopped)")
            self.status_label.setStyleSheet("color: #666;")
        
        # 执行日志监控命令
        self.cli_integration.execute_openclaw_command_async(
            "logs --follow",
            output_callback,
            error_callback,
            done_callback
        )
    
    def stop_logging(self):
        """停止日志监控"""
        self.cli_integration.stop_command()
        self.is_logging = False
        self.start_stop_btn.setText("开始监控 (Start Monitoring)")
        self.status_label.setText("未监控 (Not Monitoring)")
        self.status_label.setStyleSheet("color: #666;")
    
    def add_log(self, line, level="INFO"):
        """添加日志行"""
        # 根据日志级别设置颜色
        format = QTextCharFormat()
        if level == "ERROR":
            format.setForeground(QColor("#dc3545"))  # 红色
        elif level == "WARN":
            format.setForeground(QColor("#ffc107"))  # 黄色
        elif level == "DEBUG":
            format.setForeground(QColor("#17a2b8"))  # 青色
        else:  # INFO
            format.setForeground(QColor("#28a745"))  # 绿色
        
        # 添加日志到文本框
        cursor = self.log_text.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(line + "\n", format)
        
        # 自动滚动到底部
        self.log_text.ensureCursorVisible()
    
    def clear_logs(self):
        """清除日志"""
        self.log_text.clear()
    
    def filter_logs(self):
        """过滤日志"""
        # 这里可以实现日志过滤功能
        # 由于实时日志，过滤功能可能需要在添加日志时进行
        pass