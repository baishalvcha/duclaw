#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业仪表盘模块 - 集成系统监控和快速操作
"""

import sys
import random
from datetime import datetime, timedelta
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QPushButton, QLabel, QProgressBar, QTableWidget,
                              QTableWidgetItem, QHeaderView, QFrame, QGridLayout)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QLinearGradient, QBrush
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6 import QtCharts

class DashboardPro(QWidget):
    """专业仪表盘"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cpu_data = []
        self.memory_data = []
        self.disk_data = []
        self.network_data = []
        self.init_ui()
        self.start_monitoring()
        
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 标题
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
        
        # 系统状态卡片
        status_cards = self.create_status_cards()
        layout.addLayout(status_cards)
        
        # 图表区域
        charts_layout = QHBoxLayout()
        
        # CPU使用率图表
        cpu_chart = self.create_cpu_chart()
        charts_layout.addWidget(cpu_chart)
        
        # 内存使用率图表
        memory_chart = self.create_memory_chart()
        charts_layout.addWidget(memory_chart)
        
        layout.addLayout(charts_layout)
        
        # 快速操作和最近活动
        bottom_layout = QHBoxLayout()
        
        # 快速操作
        quick_actions = self.create_quick_actions()
        bottom_layout.addWidget(quick_actions, 1)
        
        # 最近活动
        recent_activity = self.create_recent_activity()
        bottom_layout.addWidget(recent_activity, 2)
        
        layout.addLayout(bottom_layout)
        
        # 更新时间显示
        self.update_time_label = QLabel("最后更新: --:--:--")
        self.update_time_label.setStyleSheet("color: #7f8c8d; font-size: 12px; text-align: center;")
        layout.addWidget(self.update_time_label)
        
        # 更新时间定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_dashboard)
        self.update_timer.start(2000)  # 每2秒更新一次
        
    def create_status_cards(self):
        """创建系统状态卡片"""
        cards_layout = QGridLayout()
        
        # CPU状态卡片
        cpu_card = self.create_status_card("CPU使用率", "75%", "#e74c3c", "🖥️")
        cards_layout.addWidget(cpu_card, 0, 0)
        
        # 内存状态卡片
        memory_card = self.create_status_card("内存使用", "62%", "#3498db", "💾")
        cards_layout.addWidget(memory_card, 0, 1)
        
        # 磁盘状态卡片
        disk_card = self.create_status_card("磁盘空间", "45%", "#2ecc71", "💿")
        cards_layout.addWidget(disk_card, 0, 2)
        
        # 网络状态卡片
        network_card = self.create_status_card("网络状态", "正常", "#9b59b6", "🌐")
        cards_layout.addWidget(network_card, 0, 3)
        
        # OpenClaw状态卡片
        openclaw_card = self.create_status_card("OpenClaw", "运行中", "#f39c12", "🤖")
        cards_layout.addWidget(openclaw_card, 1, 0)
        
        # Gateway状态卡片
        gateway_card = self.create_status_card("Gateway", "运行中", "#1abc9c", "🚪")
        cards_layout.addWidget(gateway_card, 1, 1)
        
        # 通道状态卡片
        channel_card = self.create_status_card("活跃通道", "3/8", "#e67e22", "📡")
        cards_layout.addWidget(channel_card, 1, 2)
        
        # 模型状态卡片
        model_card = self.create_status_card("可用模型", "5", "#34495e", "🧠")
        cards_layout.addWidget(model_card, 1, 3)
        
        return cards_layout
        
    def create_status_card(self, title, value, color, icon):
        """创建状态卡片"""
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
            }}
            QFrame:hover {{
                border-color: {color};
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        
        # 标题和图标
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {color}; font-size: 14px;")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        card_layout.addLayout(header_layout)
        
        # 数值
        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(24)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet(f"color: {color};")
        value_label.setAlignment(Qt.AlignCenter)
        
        card_layout.addWidget(value_label)
        
        # 进度条（如果适用）
        if "%" in value:
            progress_value = int(value.replace("%", ""))
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(progress_value)
            progress_bar.setTextVisible(False)
            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    background-color: #f5f5f5;
                }}
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: 4px;
                }}
            """)
            card_layout.addWidget(progress_bar)
            
            # 状态标签
            status_text = "正常" if progress_value < 80 else "警告" if progress_value < 95 else "危险"
            status_color = "#2ecc71" if progress_value < 80 else "#f39c12" if progress_value < 95 else "#e74c3c"
            
            status_label = QLabel(status_text)
            status_label.setStyleSheet(f"""
                color: {status_color};
                font-size: 12px;
                font-weight: bold;
                padding: 2px 8px;
                background-color: {status_color}20;
                border-radius: 10px;
            """)
            status_label.setAlignment(Qt.AlignCenter)
            card_layout.addWidget(status_label)
        
        return card
        
    def create_cpu_chart(self):
        """创建CPU使用率图表"""
        chart_group = QGroupBox("CPU使用率")
        chart_layout = QVBoxLayout(chart_group)
        
        # 创建图表
        chart = QChart()
        chart.setTitle("CPU使用率趋势")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # 创建系列
        series = QtCharts.QLineSeries()
        series.setName("CPU使用率")
        
        # 添加示例数据
        for i in range(20):
            series.append(i, random.randint(30, 80))
            
        chart.addSeries(series)
        
        # 创建坐标轴
        axis_x = QtCharts.QValueAxis()
        axis_x.setRange(0, 20)
        axis_x.setTitleText("时间")
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QtCharts.QValueAxis()
        axis_y.setRange(0, 100)
        axis_y.setTitleText("使用率 (%)")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        # 创建图表视图
        chart_view = QtCharts.QChartView(chart)
        chart_view.setRenderHint(QtCharts.QChartView.Antialiasing)
        chart_view.setMinimumHeight(200)
        
        chart_layout.addWidget(chart_view)
        
        # 统计信息
        stats_layout = QHBoxLayout()
        
        avg_label = QLabel("平均: 65%")
        avg_label.setStyleSheet("color: #7f8c8d;")
        
        max_label = QLabel("峰值: 82%")
        max_label.setStyleSheet("color: #e74c3c;")
        
        current_label = QLabel("当前: 75%")
        current_label.setStyleSheet("color: #3498db; font-weight: bold;")
        
        stats_layout.addWidget(avg_label)
        stats_layout.addWidget(max_label)
        stats_layout.addWidget(current_label)
        stats_layout.addStretch()
        
        chart_layout.addLayout(stats_layout)
        
        return chart_group
        
    def create_memory_chart(self):
        """创建内存使用率图表"""
        chart_group = QGroupBox("内存使用")
        chart_layout = QVBoxLayout(chart_group)
        
        # 创建图表
        chart = QChart()
        chart.setTitle("内存使用趋势")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # 创建系列
        series = QtCharts.QLineSeries()
        series.setName("内存使用率")
        
        # 添加示例数据
        for i in range(20):
            series.append(i, random.randint(40, 70))
            
        chart.addSeries(series)
        
        # 创建坐标轴
        axis_x = QtCharts.QValueAxis()
        axis_x.setRange(0, 20)
        axis_x.setTitleText("时间")
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QtCharts.QValueAxis()
        axis_y.setRange(0, 100)
        axis_y.setTitleText("使用率 (%)")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        # 创建图表视图
        chart_view = QtCharts.QChartView(chart)
        chart_view.setRenderHint(QtCharts.QChartView.Antialiasing)
        chart_view.setMinimumHeight(200)
        
        chart_layout.addWidget(chart_view)
        
        # 统计信息
        stats_layout = QHBoxLayout()
        
        total_label = QLabel("总量: 16GB")
        total_label.setStyleSheet("color: #7f8c8d;")
        
        used_label = QLabel("已用: 9.8GB")
        used_label.setStyleSheet("color: #e74c3c;")
        
        free_label = QLabel("可用: 6.2GB")
        free_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
        
        stats_layout.addWidget(total_label)
        stats_layout.addWidget(used_label)
        stats_layout.addWidget(free_label)
        stats_layout.addStretch()
        
        chart_layout.addLayout(stats_layout)
        
        return chart_group
        
    def create_quick_actions(self):
        """创建快速操作面板"""
        actions_group = QGroupBox("快速操作")
        actions_layout = QVBoxLayout(actions_group)
        
        # 操作按钮
        actions = [
            ("🚀 启动OpenClaw", "#2ecc71", self.start_openclaw),
            ("⏹️ 停止OpenClaw", "#e74c3c", self.stop_openclaw),
            ("🔄 重启Gateway", "#3498db", self.restart_gateway),
            ("🔍 运行诊断", "#f39c12", self.run_diagnosis),
            ("📊 查看日志", "#9b59b6", self.view_logs),
            ("⚙️ 系统设置", "#34495e", self.open_settings)
        ]
        
        for text, color, callback in actions:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    padding: 12px;
                    border-radius: 6px;
                    font-weight: bold;
                    text-align: left;
                    padding-left: 20px;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
            """)
            btn.clicked.connect(callback)
            actions_layout.addWidget(btn)
            
        actions_layout.addStretch()
        
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
        # 简单的颜色加深逻辑
        if color == "#2ecc71": return "#27ae60"  # 绿色
        elif color == "#e74c3c": return "#c0392b"  # 红色
        elif color == "#3498db": return "#2980b9"  # 蓝色
        elif color == "#f39c12": return "#d35400"  # 橙色
        elif color == "#9b59b6": return "#8e44ad"  # 紫色
        elif color == "#34495e": return "#2c3e50"  # 深蓝
        else: return color
        
    def start_monitoring(self):
        """开始监控"""
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_monitoring_data)
        self.monitor_timer.start(1000)  # 每秒更新监控数据
        
    def update_monitoring_data(self):
        """更新监控数据"""
        # 模拟数据更新
        self.cpu_data.append(random.randint(30, 85))
        self.memory_data.append(random.randint(40, 75))
        self.disk_data.append(random.randint(35, 65))
        self.network_data.append(random.randint(10, 100))
        
        # 保持数据长度
        if len(self.cpu_data) > 50:
            self.cpu_data = self.cpu_data[-50:]
            self.memory_data = self.memory_data[-50:]
            self.disk_data = self.disk_data[-50:]
            self.network_data = self.network_data[-50:]
            
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
        
    def run_diagnosis(self):
        """运行诊断"""
        print("运行诊断")
        
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
    window = DashboardPro()
    window.setWindowTitle("专业仪表盘测试")
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())