#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信号灯版仪表盘 - 系统状态做成信号灯，点击显示数值
"""

import sys
import random
from datetime import datetime, timedelta
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QPushButton, QLabel, QProgressBar, QTableWidget,
                              QTableWidgetItem, QHeaderView, QFrame, QGridLayout,
                              QToolButton, QMenu)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor, QPainter, QBrush, QPen, QMouseEvent

class TrafficLightWidget(QFrame):
    """信号灯小部件"""
    
    def __init__(self, name, value, color, icon, parent=None):
        super().__init__(parent)
        self.name = name
        self.value = value
        self.color = color
        self.icon = icon
        self.is_clicked = False
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 5px;
                min-width: 50px;
                min-height: 50px;
                margin: 2px;
            }}
            QFrame:hover {{
                border-color: {self.color};
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # 信号灯图标
        self.light_label = QLabel(self.icon)
        self.light_label.setStyleSheet("font-size: 20px;")
        self.light_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.light_label)
        
        # 名称标签
        self.name_label = QLabel(self.name)
        self.name_label.setStyleSheet(f"color: {self.color}; font-size: 10px; font-weight: bold;")
        self.name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.name_label)
        
        # 数值标签（初始隐藏）
        self.value_label = QLabel(self.value)
        self.value_label.setStyleSheet(f"color: {self.color}; font-size: 12px; font-weight: bold;")
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.hide()
        layout.addWidget(self.value_label)
        
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.toggle_value_display()
            
    def toggle_value_display(self):
        """切换数值显示"""
        if self.is_clicked:
            self.value_label.hide()
            self.is_clicked = False
        else:
            self.value_label.show()
            self.is_clicked = True
            
    def update_value(self, new_value):
        """更新数值"""
        self.value = new_value
        self.value_label.setText(new_value)

class DashboardTrafficLights(QWidget):
    """信号灯版仪表盘"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.traffic_lights = []
        self.init_ui()
        self.start_monitoring()
        
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 标题和信号灯区域
        header_layout = QHBoxLayout()
        
        # 标题
        title_label = QLabel("系统仪表盘")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # 信号灯区域（放在右上角）
        traffic_lights_layout = QHBoxLayout()
        
        # 定义信号灯
        lights = [
            ("CPU", "75%", "#e74c3c", "🖥️"),
            ("内存", "62%", "#3498db", "💾"),
            ("磁盘", "45%", "#2ecc71", "💿"),
            ("网络", "正常", "#9b59b6", "🌐"),
            ("Gateway", "运行中", "#1abc9c", "🚪"),
            ("通道", "3/8", "#e67e22", "📡")
        ]
        
        for name, value, color, icon in lights:
            light = TrafficLightWidget(name, value, color, icon)
            self.traffic_lights.append(light)
            traffic_lights_layout.addWidget(light)
            
        header_layout.addLayout(traffic_lights_layout)
        
        layout.addLayout(header_layout)
        
        # 调试日志（放在中间）
        debug_log = self.create_debug_log()
        layout.addWidget(debug_log)
        
        # 快速操作（放在最下面）
        quick_actions = self.create_quick_actions()
        layout.addWidget(quick_actions)
        
        # 更新时间显示
        self.update_time_label = QLabel("最后更新: --:--:--")
        self.update_time_label.setStyleSheet("color: #7f8c8d; font-size: 12px; text-align: center;")
        layout.addWidget(self.update_time_label)
        
        # 更新时间定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_dashboard)
        self.update_timer.start(2000)  # 每2秒更新一次
        
    def create_debug_log(self):
        """创建调试日志面板"""
        log_group = QGroupBox("调试日志（最近活动）")
        log_layout = QVBoxLayout(log_group)
        
        # 日志操作按钮
        log_buttons_layout = QHBoxLayout()
        
        # 复制日志按钮
        copy_btn = QPushButton("📋 复制")
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        copy_btn.clicked.connect(self.copy_debug_log)
        log_buttons_layout.addWidget(copy_btn)
        
        # 清空日志按钮
        clear_btn = QPushButton("🗑️ 清空")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        clear_btn.clicked.connect(self.clear_debug_log)
        log_buttons_layout.addWidget(clear_btn)
        
        log_buttons_layout.addStretch()
        log_layout.addLayout(log_buttons_layout)
        
        # 日志表格
        self.debug_table = QTableWidget()
        self.debug_table.setColumnCount(4)
        self.debug_table.setHorizontalHeaderLabels(["时间", "类型", "描述", "状态"])
        self.debug_table.horizontalHeader().setStretchLastSection(True)
        self.debug_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.debug_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # 设置列宽
        self.debug_table.setColumnWidth(0, 120)  # 时间
        self.debug_table.setColumnWidth(1, 80)   # 类型
        self.debug_table.setColumnWidth(2, 300)  # 描述
        
        log_layout.addWidget(self.debug_table)
        
        # 加载示例日志数据
        self.load_debug_log_data()
        
        return log_group
        
    def load_debug_log_data(self):
        """加载调试日志数据"""
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
        
        self.debug_table.setRowCount(len(logs))
        
        for i, log in enumerate(logs):
            # 时间
            time_item = QTableWidgetItem(log["time"])
            self.debug_table.setItem(i, 0, time_item)
            
            # 类型
            type_item = QTableWidgetItem(log["type"])
            if log["type"] == "启动":
                type_item.setForeground(QColor("#2ecc71"))
            elif log["type"] == "错误":
                type_item.setForeground(QColor("#e74c3c"))
            elif log["type"] == "警告":
                type_item.setForeground(QColor("#f39c12"))
            self.debug_table.setItem(i, 1, type_item)
            
            # 描述
            desc_item = QTableWidgetItem(log["description"])
            self.debug_table.setItem(i, 2, desc_item)
            
            # 状态
            status_item = QTableWidgetItem(log["status"])
            if "成功" in log["status"]:
                status_item.setForeground(QColor("#2ecc71"))
            elif "警告" in log["status"]:
                status_item.setForeground(QColor("#f39c12"))
            elif "失败" in log["status"]:
                status_item.setForeground(QColor("#e74c3c"))
            self.debug_table.setItem(i, 3, status_item)
            
    def copy_debug_log(self):
        """复制调试日志"""
        import pyperclip
        
        try:
            log_text = ""
            for i in range(self.debug_table.rowCount()):
                row_text = []
                for j in range(self.debug_table.columnCount()):
                    item = self.debug_table.item(i, j)
                    if item:
                        row_text.append(item.text())
                log_text += " | ".join(row_text) + "\n"
                
            if log_text:
                pyperclip.copy(log_text)
                self.add_log_entry("调试日志已复制到剪贴板", "INFO")
            else:
                self.add_log_entry("调试日志为空", "WARNING")
        except ImportError:
            self.add_log_entry("需要安装pyperclip库: pip install pyperclip", "ERROR")
        except Exception as e:
            self.add_log_entry(f"复制失败: {str(e)}", "ERROR")
            
    def clear_debug_log(self):
        """清空调试日志"""
        self.debug_table.setRowCount(0)
        self.add_log_entry("调试日志已清空", "INFO")
        
    def add_log_entry(self, description, log_type):
        """添加日志条目"""
        current_row = self.debug_table.rowCount()
        self.debug_table.insertRow(current_row)
        
        # 时间
        time_item = QTableWidgetItem(datetime.now().strftime("%H:%M:%S"))
        self.debug_table.setItem(current_row, 0, time_item)
        
        # 类型
        type_item = QTableWidgetItem("操作")
        if log_type == "INFO":
            type_item.setForeground(QColor("#3498db"))
        elif log_type == "WARNING":
            type_item.setForeground(QColor("#f39c12"))
        elif log_type == "ERROR":
            type_item.setForeground(QColor("#e74c3c"))
        self.debug_table.setItem(current_row, 1, type_item)
        
        # 描述
        desc_item = QTableWidgetItem(description)
        self.debug_table.setItem(current_row, 2, desc_item)
        
        # 状态
        status_item = QTableWidgetItem("✅ 完成")
        status_item.setForeground(QColor("#2ecc71"))
        self.debug_table.setItem(current_row, 3, status_item)
        
        # 滚动到底部
        self.debug_table.scrollToBottom()
        
    def create_quick_actions(self):
        """创建快速操作面板（按当前版本执行）"""
        actions_group = QGroupBox("快速操作")
        actions_layout = QVBoxLayout(actions_group)
        
        # 第一行操作
        row1_layout = QHBoxLayout()
        
        actions_row1 = [
            ("🚀 启动OpenClaw", "#2ecc71", self.start_openclaw),
            ("⏹️ 停止OpenClaw", "#e74c3c", self.stop_openclaw),
            ("🔄 重启Gateway", "#3498db", self.restart_gateway),
            ("🔧 修复故障", "#f39c12", self.repair_fault)
        ]
        
        for text, color, callback in actions_row1:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 6px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
            """)
            btn.clicked.connect(callback)
            row1_layout.addWidget(btn)
            
        actions_layout.addLayout(row1_layout)
        
        # 第二行操作
        row2_layout = QHBoxLayout()
        
        actions_row2 = [
            ("🔍 运行诊断", "#9b59b6", self.run_diagnosis),
            ("📡 测试连接", "#e67e22", self.test_connection),
            ("📊 查看日志", "#34495e", self.view_logs),
            ("⚙️ 系统设置", "#7f8c8d", self.open_settings)
        ]
        
        for text, color, callback in actions_row2:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 6px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
            """)
            btn.clicked.connect(callback)
            row2_layout.addWidget(btn)
            
        actions_layout.addLayout(row2_layout)
        
        return actions_group
        
    def get_current_time(self):
        """获取当前时间"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def darken_color(self, color):
        """加深颜色"""
        if color == "#2ecc71": return "#27ae60"
        elif color == "#e74c3c": return "#c0392b"
        elif color == "#3498db": return "#2980b9"
        elif color == "#f39c12": return "#d35400"
        elif color == "#9b59b6": return "#8e44ad"
        elif color == "#34495e": return "#2c3e50"
        elif color == "#e67e22": return "#d35400"
        elif color == "#7f8c8d": return "#5d6d7e"
        else: return color
        
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
        gateway_status = random.choice(["运行中", "运行中", "运行中", "停止"])
        channel_active = random.randint(2, 8)
        channel_total = 8
        
        # 更新信号灯数值
        if len(self.traffic_lights) >= 6:
            self.traffic_lights[0].update_value(f"{cpu_value}%")
            self.traffic_lights[1].update_value(f"{memory_value}%")
            self.traffic_lights[2].update_value(f"{disk_value}%")
            self.traffic_lights[3].update_value(network_status)
            self.traffic_lights[4].update_value(gateway_status)
            self.traffic_lights[5].update_value(f"{channel_active}/{channel_total}")
        
    def update_dashboard(self):
        """更新仪表盘"""
        current_time = self.get_current_time()
        self.update_time_label.setText(f"最后更新: {current_time}")
        
    def start_openclaw(self):
        """启动OpenClaw"""
        self.add_log_entry("正在启动OpenClaw...", "INFO")
        print("启动OpenClaw")
        
    def stop_openclaw(self):
        """停止OpenClaw"""
        self.add_log_entry("正在停止OpenClaw...", "INFO")
        print("停止OpenClaw")
        
    def restart_gateway(self):
        """重启Gateway"""
        self.add_log_entry("正在重启Gateway...", "INFO")
        print("重启Gateway")
        
    def repair_fault(self):
        """修复故障"""
        self.add_log_entry("正在修复故障...", "INFO")
        print("修复故障")
        
    def run_diagnosis(self):
        """运行诊断"""
        self.add_log_entry("正在运行系统诊断...", "INFO")
        print("运行诊断")
        
    def test_connection(self):
        """测试连接"""
        self.add_log_entry("正在测试通道连接...", "INFO")
        print("测试连接")
        
    def view_logs(self):
        """查看日志"""
        self.add_log_entry("正在打开日志查看器...", "INFO")
        print("查看日志")
        
    def open_settings(self):
        """打开设置"""
        self.add_log_entry("正在打开系统设置...", "INFO")
        print("打开设置")

# 测试函数
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = DashboardTrafficLights()
    window.setWindowTitle("信号灯版仪表盘测试")
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())