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
from PySide6.QtGui import QFont, QColor

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

class DashboardRouterComplete(QWidget):
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
        
        # 系统日志面板
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
        
        # 快速操作面板
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
            
            # 类型
            type_item = QTableWidgetItem(log["type"])
            if log["type"] == "启动":
                type_item.setForeground(QColor("#00ff88"))
            elif log["type"] == "错误":
                type_item.setForeground(QColor("#ff5555"))
            elif log["type"] == "警告":
                type_item.setForeground(QColor("#ffaa00"))
            self.log_table.setItem(i, 1, type_item)
            
            # 描述
            desc_item = QTableWidgetItem(log["description"])
            desc_item.setForeground(QColor("#ffffff"))
            self.log_table.setItem(i, 2, desc_item)
            
            # 状态
            status_item = QTableWidgetItem(log["status"])
            if "成功" in log["status"]:
                status_item.setForeground(QColor("#00ff88"))
            elif "警告" in log["status"]:
                status_item.setForeground(QColor("#ffaa00"))
            elif "失败" in log["status"]:
                status_item.setForeground(QColor("#ff5555"))
            self.log_table.setItem(i, 3, status_item)
            
    def get_current_time(self):
        """获取当前时间"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def start_monitoring(self):
        """开始监控"""
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_monitoring_data)
        self.monitor_timer.start(1000)
        
    def update_monitoring_data(self):
        """更新监控数据"""
        # 模拟数据更新
        cpu_value = random.randint(65, 85)
        memory_value = random.randint(55, 75)
        disk_value = random.randint(40, 50)
        network_status = random.choice(["正常", "良好", "延迟"])
        gateway_status = random.choice(["运行", "运行", "运行", "停止"])
        channel_active = random.randint(2, 8)
        channel_total = 8
        model_count = random.randint(3, 7)
        openclaw_status = random.choice(["运行", "运行", "运行", "停止"])
        
        # 更新状态颜色
        cpu_color = "#00ff88" if cpu_value < 80 else "#ffaa00" if cpu_value < 95 else "#ff5555"
        memory_color = "#00aaff" if memory_value < 80 else "#ffaa00" if memory_value < 95 else "#ff5555"
        disk_color = "#00ffaa" if disk_value < 80 else "#ffaa00" if disk_value < 95 else "#ff5555"
        network_color = "#aa00ff" if network_status == "正常" else "#ffaa00" if network_status == "良好" else "#ff5555"
        gateway_color = "#ffaa00" if gateway_status == "运行" else "#ff5555"
        channel_color = "#ff5500" if channel_active > 0 else "#ff5555"
        model_color = "#ff00aa"
        openclaw_color = "#ffff00" if openclaw_status == "运行" else "#ff5555"
        
        # 更新状态部件
        if len(self.status_widgets) >= 8:
            self.status_widgets[0].update_value(f"{cpu_value}%", cpu_color)
            self.status_widgets[1].update_value(f"{memory_value}%", memory_color)
            self.status_widgets[2].update_value(f"{disk_value}%", disk_color)
            self.status_widgets[3].update_value(network_status, network_color)
            self.status_widgets[4].update_value(gateway_status, gateway_color)
            self.status_widgets[5].update_value(f"{channel_active}/{channel_total}", channel_color)
            self.status_widgets[6].update_value(f"{model_count}", model_color)
            self.status_widgets[7].update_value(openclaw_status, openclaw_color)
        
    def update_dashboard(self):
        """更新仪表盘"""
        current_time = self.get_current_time()
        self.update_label.setText(f"最后更新: {current_time}")
        
    def copy_system_log(self):
        """复制系统日志"""
        import pyperclip
        
        try:
            log_text = ""
            for i in range(self.log_table.rowCount()):
                row_text = []
                for j in range(self.log_table.columnCount()):
                    item = self.log_table.item(i, j)
                    if item:
                        row_text.append(item.text())
                log_text += " | ".join(row_text) + "\n"
                
            if log_text:
                pyperclip.copy(log_text)
                self.add_log_entry("系统日志已复制到剪贴板", "INFO")
            else:
                self.add_log_entry("系统日志为空", "WARNING")
        except ImportError:
            self.add_log_entry("需要安装pyperclip库: pip install pyperclip", "ERROR")
        except Exception as e:
            self.add_log_entry(f"复制失败: {str(e)}", "ERROR")
            
    def clear_system_log(self):
        """清空系统日志"""
        self.log_table.setRowCount(0)
        self.add_log_entry("系统日志已清空", "INFO")
        
    def add_log_entry(self, description, log_type):
        """添加日志条目"""
        current_row = self.log_table.rowCount()
        self.log_table.insertRow(current_row)
        
        # 时间
        time_item = QTableWidgetItem(datetime.now().strftime("%H:%M:%S"))
        time_item.setForeground(QColor("#a0a0c0"))
        self.log_table.setItem(current_row, 0, time_item)
        
        # 类型
        type_item = QTableWidgetItem("操作")
        if log_type == "INFO":
            type_item.setForeground(QColor("#00aaff"))
        elif log_type == "WARNING":
            type_item.setForeground(QColor("#ffaa00"))
        elif log_type == "ERROR":
            type_item.setForeground(QColor("#ff5555"))
        self.log_table.setItem(current_row, 1, type_item)
        
        # 描述
        desc_item = QTableWidgetItem(description)
        desc_item.setForeground(QColor("#ffffff"))
        self.log_table.setItem(current_row, 2, desc_item)
        
        # 状态
        status_item = QTableWidgetItem("✅ 完成")
        status_item.setForeground(QColor("#00ff88"))
        self.log_table.setItem(current_row, 3, status_item)
        
        # 滚动到底部
        self.log_table.scrollToBottom()
        
    def start_system(self):
        """启动系统"""
        self.add_log_entry("正在启动OpenClaw系统...", "INFO")
        print("启动系统")
        
    def stop_system(self):
        """停止系统"""
        self.add_log_entry("正在停止OpenClaw系统...", "INFO")
        print("停止系统")
        
    def restart_service(self):
        """重启服务"""
        self.add_log_entry("正在重启Gateway服务...", "INFO")
        print("重启服务")
        
    def system_diagnosis(self):
        """系统诊断"""
        self.add_log_entry("正在运行系统诊断...", "INFO")
        print("系统诊断")
        
    def view_statistics(self):
        """查看统计"""
        self.add_log_entry("正在打开系统统计...", "INFO")
        print("查看统计")
        
    def system_settings(self):
        """系统设置"""
        self.add_log_entry("正在打开系统设置...", "INFO")
        print("系统设置")
        
    def view_logs(self):
        """查看日志"""
        self.add_log_entry("正在打开日志查看器...", "INFO")
        print("查看日志")
        
    def network_status(self):
        """网络状态"""
        self.add_log_entry("正在查看网络状态...", "INFO")
        print("网络状态")

# 测试函数
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = DashboardRouterComplete()
    window.setWindowTitle("路由器风格仪表盘测试")
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())