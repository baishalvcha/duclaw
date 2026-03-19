#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路由器风格仪表盘 - 类似网络设备界面
"""

import sys
import random
from datetime import datetime, timedelta
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QPushButton, QLabel, QTableWidget,
                              QTableWidgetItem, QHeaderView, QFrame, QGridLayout)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QLinearGradient, QBrush, QPainter

class RouterStatusWidget(QFrame):
    """路由器状态小部件"""
    
    def __init__(self, name, value, status_color, icon, parent=None):
        super().__init__(parent)
        self.name = name
        self.value = value
        self.status_color = status_color
        self.icon = icon
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #1a1a2e;
                border: 1px solid #2d2d4d;
                border-radius: 6px;
                padding: 8px;
                min-width: 80px;
                min-height: 80px;
                margin: 2px;
            }}
            QFrame:hover {{
                border-color: {self.status_color};
                box-shadow: 0 0 8px {self.status_color}80;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(4)
        
        # 状态指示灯
        self.status_light = QLabel("●")
        self.status_light.setStyleSheet(f"""
            color: {self.status_color};
            font-size: 20px;
            font-weight: bold;
        """)
        self.status_light.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_light)
        
        # 图标
        self.icon_label = QLabel(self.icon)
        self.icon_label.setStyleSheet("color: #ffffff; font-size: 18px;")
        self.icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_label)
        
        # 名称
        self.name_label = QLabel(self.name)
        self.name_label.setStyleSheet("color: #a0a0c0; font-size: 10px; font-weight: bold;")
        self.name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.name_label)
        
        # 数值（悬停显示）
        self.value_label = QLabel(self.value)
        self.value_label.setStyleSheet(f"""
            color: {self.status_color};
            font-size: 12px;
            font-weight: bold;
            background-color: {self.status_color}20;
            border-radius: 4px;
            padding: 2px 6px;
        """)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.hide()
        layout.addWidget(self.value_label)
        
    def enterEvent(self, event):
        """鼠标进入事件"""
        self.value_label.show()
        
    def leaveEvent(self, event):
        """鼠标离开事件"""
        self.value_label.hide()
        
    def update_value(self, new_value, new_color=None):
        """更新数值和颜色"""
        self.value = new_value
        self.value_label.setText(new_value)
        if new_color:
            self.status_color = new_color
            self.status_light.setStyleSheet(f"""
                color: {self.status_color};
                font-size: 20px;
                font-weight: bold;
            """)
            self.value_label.setStyleSheet(f"""
                color: {self.status_color};
                font-size: 12px;
                font-weight: bold;
                background-color: {self.status_color}20;
                border-radius: 4px;
                padding: 2px 6px;
            """)

class DashboardRouterStyle(QWidget):
    """路由器风格仪表盘"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.status_widgets = []
        self.init_ui()
        self.start_monitoring()
        
    def init_ui(self):
        """初始化界面"""
        # 设置主窗口背景
        self.setStyleSheet("""
            QWidget {
                background-color: #0f0f1a;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 标题栏
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a2e;
                border: 1px solid #2d2d4d;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        
        # 标题
        title_label = QLabel("OpenClaw 管理系统")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #4cc9f0;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # 时间显示
        time_label = QLabel(self.get_current_time())
        time_label.setStyleSheet("color: #a0a0c0; font-size: 14px;")
        header_layout.addWidget(time_label)
        
        layout.addWidget(header_frame)
        
        # 路由器状态面板
        status_panel = QGroupBox("系统状态")
        status_panel.setStyleSheet("""
            QGroupBox {
                background-color: #1a1a2e;
                border: 1px solid #2d2d4d;
                border-radius: 8px;
                padding: 15px;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #4cc9f0;
            }
        """)
        
        status_layout = QGridLayout(status_panel)
        
        # 定义路由器状态项
        status_items = [
            ("CPU", "75%", "#00ff88", "🖥️", 0, 0),
            ("内存", "62%", "#00aaff", "💾", 0, 1),
            ("磁盘", "45%", "#00ffaa", "💿", 0, 2),
            ("网络", "正常", "#aa00ff", "🌐", 0, 3),
            ("Gateway", "运行", "#ffaa00", "🚪", 1, 0),
            ("通道", "3/8", "#ff5500", "📡", 1, 1),
            ("模型", "5", "#ff00aa", "🧠", 1, 2),
            ("OpenClaw", "运行", "#ffff00", "🤖", 1, 3)
        ]
        
        for name, value, color, icon, row, col in status_items:
            widget = RouterStatusWidget(name, value, color, icon)
            self.status_widgets.append(widget)
            status_layout.addWidget(widget, row, col)
            
        layout.addWidget(status_panel)
        
        # 系统日志面板（路由器风格）
        log_panel = QGroupBox("系统日志")
        log_panel.setStyleSheet("""
            QGroupBox {
                background-color: #1a1a2e;
                border: 1px solid #2d2d4d;
                border-radius: 8px;
                padding: 15px;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #4cc9f0;
            }
        """)
        
        log_layout = QVBoxLayout(log_panel)
        
        # 日志操作按钮
        log_buttons_layout = QHBoxLayout()
        
        # 复制日志按钮
        copy_btn = QPushButton("📋 复制日志")
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #4cc9f0;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #4cc9f0;
                color: #0f0f1a;
            }
        """)
        copy_btn.clicked.connect(self.copy_system_log)
        log_buttons_layout.addWidget(copy_btn)
        
        # 清空日志按钮
        clear_btn = QPushButton("🗑️ 清空日志")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #ff5555;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #ff5555;
                color: #0f0f1a;
            }
        """)
        clear_btn.clicked.connect(self.clear_system_log)
        log_buttons_layout.addWidget(clear_btn)
        
        log_buttons_layout.addStretch()
        log_layout.addLayout(log_buttons_layout)
        
        # 日志表格
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(4)
        self.log_table.setHorizontalHeaderLabels(["时间", "类型", "描述", "状态"])
        
        # 设置表格样式
        self.log_table.setStyleSheet("""
            QTableWidget {
                background-color: #0f0f1a;
                border: 1px solid #2d2d4d;
                color: #ffffff;
                gridline-color: #2d2d4d;
            }
            QHeaderView::section {
                background-color: #1a1a2e;
                color: #4cc9f0;
                border: 1px solid #2d2d4d;
                padding: 5px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        
        self.log_table.horizontalHeader().setStretchLastSection(True)
        self.log_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.log_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # 设置列宽
        self.log_table.setColumnWidth(0, 120)  # 时间
        self.log_table.setColumnWidth(1, 80)   # 类型
        self.log_table.setColumnWidth(2, 300)  # 描述
        
        log_layout.addWidget(self.log_table)
        
        layout.addWidget(log_panel)
        
        # 快速操作面板（路由器风格）
        actions_panel = QGroupBox("快速操作")
        actions_panel.setStyleSheet("""
            QGroupBox {
                background-color: #1a1a2e;
                border: 1px solid #2d2d4d;
                border-radius: 8px;
                padding: 15px;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #4cc9f0;
            }
        """)
        
        actions_layout = QVBoxLayout(actions_panel)
        
        # 第一行操作
        row1_layout = QHBoxLayout()
        
        actions_row1 = [
            ("🚀 启动系统", "#00ff88", self.start_system),
            ("⏹️ 停止系统", "#ff5555", self.stop_system),
            ("🔄 重启服务", "#00aaff", self.restart_service),
            ("🔧 系统诊断", "#ffaa00", self.system_diagnosis)
        ]
        
        for text, color, callback in actions_row1:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #2d2d4d;
                    color: #ffffff;
                    border: 1px solid {color};
                    padding: 10px;
                    border-radius: 6px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    color: #0f0f1a;
                }}
            """)
            btn.clicked.connect(callback)
            row1_layout.addWidget(btn)
            
        actions_layout.addLayout(row1_layout)
        
        # 第二行操作
        row2_layout = QHBoxLayout()
        
        actions_row2 = [
            ("📊 查看统计", "#aa00ff", self.view_statistics),
            ("⚙️ 系统设置", "#a0a0c0", self.system_settings),
            ("🔍 查看日志", "#ffff00", self.view_logs),
            ("📡 网络状态", "#00ffaa", self.network_status)
        ]
        
        for text, color, callback in actions_row2:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #2d2d4d;
                    color: #ffffff;
                    border: 1px solid {color};
                    padding: 10px;
                    border-radius: 6px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    color: #0f0f1a;
                }}
            """)
            btn.clicked.connect(callback)
            row2_layout.addWidget(btn)
            
        actions_layout.addLayout(row2_layout)
        
        layout.addWidget(actions_panel)
        
        # 状态栏
        status_bar = QFrame()
        status_bar.setStyleSheet("""
            QFrame {
                background-color: #1a1a2e;
                border: 1px solid #2d2d4d;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        
        status_bar_layout = QHBoxLayout(status_bar)
        
        self.status_label = QLabel("系统运行正常")
        self.status_label.setStyleSheet("color: #00ff88; font-size: 12px;")
        
        self.update_label = QLabel("最后更新: --:--:--")
        self.update_label.setStyleSheet("color: #a0a0c0; font-size: 12px;")
        
        status_bar_layout.addWidget(self.status_label)
        status_bar_layout.addStretch()
        status_bar_layout.addWidget(self.update_label)
        
        layout.addWidget(status_bar)
        
        # 加载系统日志数据
        self.load_system_log_data()
        
        # 更新时间定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_dashboard)
        self.update_timer.start(2000)  # 每2秒更新一次
        
    def load_system_log_data(self):
        """加载系统日志数据"""
        logs = [
            {
                "time": (datetime.now() - timedelta(minutes=5)).strftime("%H:%M:%S"),
                "type": "启动",
                "description": "OpenClaw Gateway服务启动成功",
                "status": "✅ 成功"
            },
            {
                "time": (datetime.now() - timedelta(minutes=12)).strftime("%H:%M:%S"),
                "type": "连接",
                "description": "QQ Bot通道连接建立",
                "status": "✅ 成功"
            },
            {
                "time": (datetime.now() - timedelta(minutes=25)).strftime("%H:%M:%S"),
                "type": "配置",
                "description": "飞书应用权限更新",
                "status": "⚠️ 警告"
            },
            {
                "time": (datetime.now() - timedelta(minutes=40)).strftime("%H:%M:%S"),
                "type": "诊断",
                "description": "系统健康检查完成",
                "status": "✅ 成功"
            },
            {
                "time": (datetime.now() - timedelta(minutes=55)).strftime("%H:%M:%S"),
                "type": "错误",
                "description": "微信通道连接超时",
                "status": "❌ 失败"
            },
            {
                "time": (datetime.now() - timedelta(hours=1, minutes=10)).strftime("%H:%M:%S"),
                "type": "备份",
                "description": "系统配置自动备份",
                "status": "✅ 成功"
            },
            {
                "time": (datetime.now() - timedelta(hours=1, minutes=30)).strftime("%H:%M:%S"),
                "type": "更新",
                "description": "模型配置同步完成",
                "status": "✅ 成功"
            }
        ]
        
        self.log_table.setRowCount(len(logs))
        
        for i, log in enumerate(logs):
            # 时间
            time_item = QTableWidgetItem(log["time"])
            time_item.setForeground(QColor("#a0a0c0"))
            self.log_table.setItem(i, 0, time_item)
            
            #