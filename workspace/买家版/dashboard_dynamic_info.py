#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态信息形状仪表盘 - 使用信息卡片代替进度条
"""

import sys
import random
from datetime import datetime, timedelta
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QPushButton, QLabel, QProgressBar, QTableWidget,
                              QTableWidgetItem, QHeaderView, QFrame, QGridLayout)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QPainter, QBrush, QPen
from PySide6.QtCore import QRectF

class DashboardDynamicInfo(QWidget):
    """动态信息形状仪表盘"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.start_monitoring()
        
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 标题和时间
        title_layout = QHBoxLayout()
        
        title_label = QLabel("系统仪表盘")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        
        time_label = QLabel(self.get_current_time())
        time_label.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(time_label)
        
        layout.addLayout(title_layout)
        
        # 顶部小图标区域
        top_icons = self.create_top_icons()
        layout.addLayout(top_icons)
        
        # 动态信息形状区域（代替进度条）
        dynamic_info = self.create_dynamic_info()
        layout.addWidget(dynamic_info)
        
        # 最近活动
        recent_activity = self.create_recent_activity()
        layout.addWidget(recent_activity)
        
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
        
    def create_top_icons(self):
        """创建顶部小图标区域"""
        icons_layout = QHBoxLayout()
        
        # 定义图标和颜色
        icons = [
            ("🖥️", "CPU", "75%", "#e74c3c"),
            ("💾", "内存", "62%", "#3498db"),
            ("💿", "磁盘", "45%", "#2ecc71"),
            ("🌐", "网络", "正常", "#9b59b6"),
            ("🤖", "OpenClaw", "运行中", "#f39c12"),
            ("🚪", "Gateway", "运行中", "#1abc9c"),
            ("📡", "通道", "3/8", "#e67e22"),
            ("🧠", "模型", "5", "#34495e")
        ]
        
        for icon, title, value, color in icons:
            icon_widget = self.create_icon_widget(icon, title, value, color)
            icons_layout.addWidget(icon_widget)
            
        return icons_layout
        
    def create_icon_widget(self, icon, title, value, color):
        """创建单个图标小部件"""
        widget = QFrame()
        widget.setFrameShape(QFrame.StyledPanel)
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 8px;
                min-width: 70px;
                min-height: 70px;
                margin: 2px;
            }}
            QFrame:hover {{
                border-color: {color};
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
        """)
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # 图标
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 20px;")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 数值（初始隐藏）
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignCenter)
        value_label.hide()  # 初始隐藏
        layout.addWidget(value_label)
        
        # 存储引用
        widget.value_label = value_label
        
        # 鼠标悬停事件
        widget.enterEvent = lambda event, w=widget, vl=value_label: self.on_icon_hover_enter(w, vl)
        widget.leaveEvent = lambda event, w=widget, vl=value_label: self.on_icon_hover_leave(w, vl)
        
        return widget
        
    def on_icon_hover_enter(self, widget, value_label):
        """鼠标进入图标区域"""
        value_label.show()
        
    def on_icon_hover_leave(self, widget, value_label):
        """鼠标离开图标区域"""
        value_label.hide()
        
    def create_dynamic_info(self):
        """创建动态信息形状区域"""
        info_group = QGroupBox("资源使用情况")
        info_layout = QGridLayout(info_group)
        
        # CPU信息卡片
        cpu_card = self.create_info_card("CPU使用率", "75%", "核心: 8/8", "温度: 65°C", "#e74c3c", "🖥️")
        info_layout.addWidget(cpu_card, 0, 0)
        
        # 内存信息卡片
        memory_card = self.create_info_card("内存使用", "62%", "已用: 9.8GB", "可用: 6.2GB", "#3498db", "💾")
        info_layout.addWidget(memory_card, 0, 1)
        
        # 磁盘信息卡片
        disk_card = self.create_info_card("磁盘空间", "45%", "已用: 225GB", "可用: 275GB", "#2ecc71", "💿")
        info_layout.addWidget(disk_card, 0, 2)
        
        # 网络信息卡片
        network_card = self.create_info_card("网络状态", "正常", "上行: 1.2MB/s", "下行: 3.5MB/s", "#9b59b6", "🌐")
        info_layout.addWidget(network_card, 0, 3)
        
        # 动态数据标签
        self.cpu_value_label = QLabel("75%")
        self.cpu_value_label.setStyleSheet("color: #e74c3c; font-size: 24px; font-weight: bold;")
        self.cpu_value_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.cpu_value_label, 1, 0)
        
        self.memory_value_label = QLabel("62%")
        self.memory_value_label.setStyleSheet("color: #3498db; font-size: 24px; font-weight: bold;")
        self.memory_value_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.memory_value_label, 1, 1)
        
        self.disk_value_label = QLabel("45%")
        self.disk_value_label.setStyleSheet("color: #2ecc71; font-size: 24px; font-weight: bold;")
        self.disk_value_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.disk_value_label, 1, 2)
        
        self.network_value_label = QLabel("正常")
        self.network_value_label.setStyleSheet("color: #9b59b6; font-size: 24px; font-weight: bold;")
        self.network_value_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.network_value_label, 1, 3)
        
        return info_group
        
    def create_info_card(self, title, value, detail1, detail2, color, icon):
        """创建信息卡片"""
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 12px;
                padding: 15px;
                min-width: 180px;
                min-height: 120px;
            }}
            QFrame:hover {{
                background-color: {color}10;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        # 标题行
        title_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {color}; font-size: 16px;")
        
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # 主数值
        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(28)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet(f"color: {color};")
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)
        
        # 详细信息
        details_layout = QVBoxLayout()
        
        detail1_label = QLabel(detail1)
        detail1_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        detail1_label.setAlignment(Qt.AlignCenter)
        details_layout.addWidget(detail1_label)
        
        detail2_label = QLabel(detail2)
        detail2_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        detail2_label.setAlignment(Qt.AlignCenter)
        details_layout.addWidget(detail2_label)
        
        layout.addLayout(details_layout)
        
        return card
        
    def create_quick_actions(self):
        """创建快速操作面板（包含测试连接）"""
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
        
    def create_recent_activity(self):
        """创建最近活动面板"""
        activity_group = QGroupBox("最近活动")
        activity_layout = QVBoxLayout(activity_group)
        
        # 活动表格
        self.activity_table = QTableWidget()
        self.activity_table.setColumnCount(4)
        self.activity_table.setHorizontalHeaderLabels(["时间", "类型", "描述", "状态"])
        self.activity_table.horizontalHeader().setStretchLastSection(True)
        self.activity_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.activity_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # 设置列宽
        self.activity_table.setColumnWidth(0, 120)  # 时间
        self.activity_table.setColumnWidth(1, 80)   # 类型
        self.activity_table.setColumnWidth(2, 300)  # 描述
        
        activity_layout.addWidget(self.activity_table)
        
        # 加载示例活动数据
        self.load_activity_data()
        
        return activity_group
        
    def load_activity_data(self):
        """加载活动数据"""
        activities = [
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
        
        self.activity_table.setRowCount(len(activities))
        
        for i, activity in enumerate(activities):
            # 时间
            time_item = QTableWidgetItem(activity["time"])
            self.activity_table.setItem(i, 0, time_item)
            
            # 类型
            type_item = QTableWidgetItem(activity["type"])
            if activity["type"] == "启动":
                type_item.setForeground(QColor("#2ecc71"))
            elif activity["type"] == "错误":
                type_item.setForeground(QColor("#e74c3c"))
            elif activity["type"] == "警告":
                type_item.setForeground(QColor("#f39c12"))
            self.activity_table.setItem(i, 1, type_item)
            
            # 描述
            desc_item = QTableWidgetItem(activity["description"])
            self.activity_table.setItem(i, 2, desc_item)
            
            # 状态
            status_item = QTableWidgetItem(activity["status"])
            if "成功" in activity["status"]:
                status_item.setForeground(QColor("#2ecc71"))
            elif "警告" in activity["status"]:
                status_item.setForeground(QColor("#f39c12"))
            elif "失败" in activity["status"]:
                status_item.setForeground(QColor("#e74c3c"))
            self.activity_table.setItem(i, 3, status_item)
            
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
        
        # 更新标签
        self.cpu_value_label.setText(f"{cpu_value}%")
        self.memory_value_label.setText(f"{memory_value}%")
        self.disk_value_label.setText(f"{disk_value}%")
        self.network_value_label.setText(network_status)
        
    def update_dashboard(self):
        """更新仪表盘"""
        current_time = self.get_current_time()
        self.update_time_label.setText(f"最后更新: {current_time}")
        
    def start_openclaw(self):
        """启动OpenClaw"""
        print("启动OpenClaw")
        
    def stop_openclaw(self):
        """停止OpenClaw"""
        print("停止OpenClaw")
        
    def restart_gateway(self):
        """重启Gateway"""
        print("重启Gateway")
        
    def repair_fault(self):
        """修复故障"""
        print("修复故障")
        
    def run_diagnosis(self):
        """运行诊断"""
        print("运行诊断")
        
    def test_connection(self):
        """测试连接"""
        print("测试连接")
        
    def view_logs(self):
        """查看日志"""
        print("查看日志")
        
    def open_settings(self):
        """打开设置"""
        print("打开设置")

# 测试函数
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = DashboardDynamicInfo()
    window.setWindowTitle("动态信息形状仪表盘测试")
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())