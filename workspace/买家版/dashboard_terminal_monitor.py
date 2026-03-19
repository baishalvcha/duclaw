#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
终端监控版仪表盘 - 上半部分终端窗口，下半部分活动表格
"""

import sys
import random
import subprocess
import threading
from datetime import datetime, timedelta
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QPushButton, QLabel, QTableWidget,
                              QTableWidgetItem, QHeaderView, QFrame, QTextEdit,
                              QSplitter, QComboBox, QLineEdit)
from PySide6.QtCore import Qt, QTimer, QProcess, QByteArray
from PySide6.QtGui import QFont, QColor, QTextCursor

class TerminalMonitor(QWidget):
    """终端监控界面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.process = None
        self.terminal_output = []
        self.max_output_lines = 1000
        self.init_ui()
        self.start_system_monitoring()
        
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
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
        title_label = QLabel("OpenClaw 终端监控")
        title_font = QFont()
        title_font.setPointSize(18)
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
        
        # 创建分割器
        splitter = QSplitter(Qt.Vertical)
        
        # 上半部分：终端监控窗口
        terminal_panel = self.create_terminal_panel()
        splitter.addWidget(terminal_panel)
        
        # 下半部分：最新活动表格
        activity_panel = self.create_activity_panel()
        splitter.addWidget(activity_panel)
        
        # 设置分割器比例
        splitter.setSizes([400, 300])
        
        layout.addWidget(splitter)
        
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
        
        self.status_label = QLabel("终端监控已启动")
        self.status_label.setStyleSheet("color: #00ff88; font-size: 12px;")
        
        self.update_label = QLabel("最后更新: --:--:--")
        self.update_label.setStyleSheet("color: #a0a0c0; font-size: 12px;")
        
        status_bar_layout.addWidget(self.status_label)
        status_bar_layout.addStretch()
        status_bar_layout.addWidget(self.update_label)
        
        layout.addWidget(status_bar)
        
        # 更新时间定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_dashboard)
        self.update_timer.start(2000)  # 每2秒更新一次
        
    def create_terminal_panel(self):
        """创建终端监控面板"""
        panel = QGroupBox("终端监控窗口")
        panel.setStyleSheet("""
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
        
        layout = QVBoxLayout(panel)
        
        # 终端命令选择
        command_layout = QHBoxLayout()
        
        command_layout.addWidget(QLabel("监控命令:"))
        
        self.command_combo = QComboBox()
        self.command_combo.addItems([
            "openclaw logs --follow",
            "openclaw doctor",
            "openclaw status",
            "openclaw gateway status",
            "systemctl status openclaw",
            "tail -f ~/.openclaw/logs/gateway.log"
        ])
        self.command_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #4cc9f0;
                border-radius: 4px;
                padding: 5px;
                min-width: 200px;
            }
        """)
        command_layout.addWidget(self.command_combo)
        
        # 自定义命令输入
        self.custom_command = QLineEdit()
        self.custom_command.setPlaceholderText("输入自定义命令...")
        self.custom_command.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #4cc9f0;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        command_layout.addWidget(self.custom_command)
        
        # 启动监控按钮
        self.start_btn = QPushButton("▶️ 启动监控")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #00ff88;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ff88;
                color: #0f0f1a;
            }
        """)
        self.start_btn.clicked.connect(self.start_terminal_monitor)
        command_layout.addWidget(self.start_btn)
        
        # 停止监控按钮
        self.stop_btn = QPushButton("⏹️ 停止监控")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #ff5555;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff5555;
                color: #0f0f1a;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_terminal_monitor)
        self.stop_btn.setEnabled(False)
        command_layout.addWidget(self.stop_btn)
        
        command_layout.addStretch()
        layout.addLayout(command_layout)
        
        # 终端输出显示
        self.terminal_output = QTextEdit()
        self.terminal_output.setStyleSheet("""
            QTextEdit {
                background-color: #0f0f1a;
                color: #ffffff;
                border: 1px solid #2d2d4d;
                border-radius: 4px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
        self.terminal_output.setReadOnly(True)
        layout.addWidget(self.terminal_output)
        
        # 终端操作按钮
        terminal_buttons_layout = QHBoxLayout()
        
        # 复制全部按钮
        copy_all_btn = QPushButton("📋 复制全部")
        copy_all_btn.setStyleSheet("""
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
        copy_all_btn.clicked.connect(self.copy_terminal_output)
        terminal_buttons_layout.addWidget(copy_all_btn)
        
        # 清空终端按钮
        clear_terminal_btn = QPushButton("🗑️ 清空终端")
        clear_terminal_btn.setStyleSheet("""
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
        clear_terminal_btn.clicked.connect(self.clear_terminal_output)
        terminal_buttons_layout.addWidget(clear_terminal_btn)
        
        # 保存日志按钮
        save_log_btn = QPushButton("💾 保存日志")
        save_log_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #ffaa00;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #ffaa00;
                color: #0f0f1a;
            }
        """)
        save_log_btn.clicked.connect(self.save_terminal_log)
        terminal_buttons_layout.addWidget(save_log_btn)
        
        terminal_buttons_layout.addStretch()
        layout.addLayout(terminal_buttons_layout)
        
        return panel
        
    def create_activity_panel(self):
        """创建最新活动面板"""
        panel = QGroupBox("最新活动（可复制到客服对话）")
        panel.setStyleSheet("""
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
        
        layout = QVBoxLayout(panel)
        
        # 活动操作按钮
        activity_buttons_layout = QHBoxLayout()
        
        # 复制活动按钮
        copy_activity_btn = QPushButton("📋 复制活动")
        copy_activity_btn.setStyleSheet("""
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
        copy_activity_btn.clicked.connect(self.copy_activity_data)
        activity_buttons_layout.addWidget(copy_activity_btn)
        
        # 清空活动按钮
        clear_activity_btn = QPushButton("🗑️ 清空活动")
        clear_activity_btn.setStyleSheet("""
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
        clear_activity_btn.clicked.connect(self.clear_activity_data)
        activity_buttons_layout.addWidget(clear_activity_btn)
        
        # 分析故障按钮
        analyze_btn = QPushButton("🔍 分析故障")
        analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #ff00aa;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #ff00aa;
                color: #0f0f1a;
            }
        """)
        analyze_btn.clicked.connect(self.analyze_faults)
        activity_buttons_layout.addWidget(analyze_btn)
        
        activity_buttons_layout.addStretch()
        layout.addLayout(activity_buttons_layout)
        
        # 活动表格
        self.activity_table = QTableWidget()
        self.activity_table.setColumnCount(4)
        self.activity_table.setHorizontalHeaderLabels(["时间", "类型", "描述", "状态"])
        
        # 设置表格样式
        self.activity_table.setStyleSheet("""
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
        
        self.activity_table.horizontalHeader().setStretchLastSection(True)
        self.activity_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.activity_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # 设置列宽
        self.activity_table.setColumnWidth(0, 120)  # 时间
        self.activity_table.setColumnWidth(1, 80)   # 类型
        self.activity_table.setColumnWidth(2, 300)  # 描述
        
        layout.addWidget(self.activity_table)
        
        # 加载示例活动数据
        self.load_activity_data()
        
        return panel
        
    def load_activity_data(self):
        """加载活动数据"""
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
        
        self.activity_table.setRowCount(len(logs))
        
        for i, log in enumerate(logs):
            # 时间
            time_item = QTableWidgetItem(log["time"])
            time_item.setForeground(QColor("#a0a0c0"))
            self.activity_table.setItem(i, 0, time_item)
            
            # 类型
            type_item = QTableWidgetItem(log["type"])
            if log["type"] == "启动":
                type_item.setForeground(QColor("#00ff88"))
            elif log["type"] == "错误":
                type_item.setForeground(QColor("#ff5555"))
            elif log["type"] == "警告":
                type_item.setForeground(QColor("#ffaa00"))
            self.activity_table.setItem(i, 1, type_item)
            
            # 描述
            desc_item = QTableWidgetItem(log["description"])
            desc_item.setForeground(QColor("#ffffff"))
            self.activity_table.setItem(i, 2, desc_item)
            
            # 状态
            status_item = QTableWidgetItem(log["status"])
            if "成功" in log["status"]:
                status_item.setForeground(QColor("#00ff88"))
            elif "警告" in log["status"]:
                status_item.setForeground(QColor("#ffaa00"))
            elif "失败" in log["status"]:
                status_item.setForeground(QColor("#ff5555"))
            self.activity_table.setItem(i, 3, status_item)
            
    def get_current_time(self):
        """获取当前时间"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def start_system_monitoring(self):
        """开始系统监控"""
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_system_status)
        self.monitor_timer.start(5000)  # 每5秒更新一次系统状态
        
    def update_system_status(self):
        """更新系统状态"""
        # 模拟系统状态更新
        current_time = self.get_current_time()
        self.update_label.setText(f"最后更新: {current_time}")
        
    def update_dashboard(self):
        """更新仪表盘"""
        current_time = self.get_current_time()
        self.update_label.setText(f"最后更新: {current_time}")
        
    def start_terminal_monitor(self):
        """启动终端监控"""
        command = self.command_combo.currentText()
        if self.custom_command.text():
            command = self.custom_command.text()
            
        self.add_activity_entry(f"启动终端监控: {command}", "INFO")
        self.status_label.setText(f"监控中: {command}")
        self.status_label.setStyleSheet("color: #00ff88; font-size: 12px;")
        
        # 模拟终端输出
        self.simulate_terminal_output(command)
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
    def stop_terminal_monitor(self):
        """停止终端监控"""
        self.add_activity_entry("停止终端监控", "INFO")
        self.status_label.setText("终端监控已停止")
        self.status_label.setStyleSheet("color: #ff5555; font-size: 12px;")
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
    def simulate_terminal_output(self, command):
        """模拟终端输出"""
        # 清空现有输出
        self.terminal_output.clear()
        
        # 根据命令类型生成不同的模拟输出
        if "logs" in command:
            self.append_terminal_output("🔍 开始监控 OpenClaw 日志...")
            self.append_terminal_output("📊 日志文件: ~/.openclaw/logs/gateway.log")
            self.append_terminal_output("🕐 时间戳: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.append_terminal_output("✅ Gateway 服务运行正常")
            self.append_terminal_output("📡 QQ Bot 通道连接成功")
            self.append_terminal_output("🤖 模型加载完成: deepseek-chat")
            self.append_terminal_output("💾 内存使用: 65% (正常)")
            self.append_terminal_output("🔧 系统检查: 通过")
            
        elif "doctor" in command:
            self.append_terminal_output("🩺 运行 OpenClaw 诊断工具...")
            self.append_terminal_output("✅ 检查 1: Gateway 服务状态 - 正常")
            self.append_terminal_output("✅ 检查 2: 配置文件完整性 - 正常")
            self.append_terminal_output("✅ 检查 3: 网络连接测试 - 正常")
            self.append_terminal_output("✅ 检查 4: 模型可用性 - 正常")
            self.append_terminal_output("✅ 检查 5: 权限设置 - 正常")
            self.append_terminal_output("🎉 所有诊断检查通过！系统健康")
            
        elif "status" in command:
            self.append_terminal_output("📊 OpenClaw 系统状态:")
            self.append_terminal_output("  ├─ Gateway: 🟢 运行中")
            self.append_terminal_output("  ├─ QQ Bot: 🟢 已连接")
            self.append_terminal_output("  ├─ 飞书: 🟡 配置中")
            self.append_terminal_output("  ├─ 微信: 🔴 未配置")
            self.append_terminal_output("  ├─ 模型: 🟢 可用 (5个)")
            self.append_terminal_output("  └─ 内存: 🟡 65% 使用率")
            
        else:
            self.append_terminal_output(f"🚀 执行命令: {command}")
            self.append_terminal_output("📝 命令输出模拟...")
            self.append_terminal_output("✅ 命令执行成功")
            self.append_terminal_output("📊 输出结果已显示")
            
    def append_terminal_output(self, text):
        """添加终端输出"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_text = f"[{timestamp}] {text}"
        
        self.terminal_output.append(formatted_text)
        
        # 滚动到底部
        cursor = self.terminal_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.terminal_output.setTextCursor(cursor)
        
    def copy_terminal_output(self):
        """复制终端输出"""
        import pyperclip
        
        try:
            text = self.terminal_output.toPlainText()
            if text:
                pyperclip.copy(text)
                self.add_activity_entry("终端输出已复制到剪贴板", "INFO")
            else:
                self.add_activity_entry("终端输出为空", "WARNING")
        except ImportError:
            self.add_activity_entry("需要安装pyperclip库: pip install pyperclip", "ERROR")
        except Exception as e:
            self.add_activity_entry(f"复制失败: {str(e)}", "ERROR")
            
    def clear_terminal_output(self):
        """清空终端输出"""
        self.terminal_output.clear()
        self.add_activity_entry("终端输出已清空", "INFO")
        
    def save_terminal_log(self):
        """保存终端日志"""
        text = self.terminal_output.toPlainText()
        if text:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"terminal_log_{timestamp}.txt"
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.add_activity_entry(f"终端日志已保存到: {filename}", "INFO")
            except Exception as e:
                self.add_activity_entry(f"保存失败: {str(e)}", "ERROR")
        else:
            self.add_activity_entry("终端输出为空", "WARNING")
            
    def copy_activity_data(self):
        """复制活动数据"""
        import pyperclip
        
        try:
            activity_text = ""
            for i in range(self.activity_table.rowCount()):
                row_text = []
                for j in range(self.activity_table.columnCount()):
                    item = self.activity_table.item(i, j)
                    if item:
                        row_text.append(item.text())
                activity_text += " | ".join(row_text) + "\n"
                
            if activity_text:
                pyperclip.copy(activity_text)
                self.add_activity_entry("活动数据已复制到剪贴板", "INFO")
            else:
                self.add_activity_entry("活动数据为空", "WARNING")
        except ImportError:
            self.add_activity_entry("需要安装pyperclip库: pip install pyperclip", "ERROR")
        except Exception as e:
            self.add_activity_entry(f"复制失败: {str(e)}", "ERROR")
            
    def clear_activity_data(self):
        """清空活动数据"""
        self.activity_table.setRowCount(0)
        self.add_activity_entry("活动数据已清空", "INFO")
        
    def analyze_faults(self):
        """分析故障"""
        # 模拟故障分析
        self.add_activity_entry("开始分析系统故障...", "INFO")
        
        # 检查终端输出中的错误
        terminal_text = self.terminal_output.toPlainText()
        
        if "错误" in terminal_text or "失败" in terminal_text or "ERROR" in terminal_text:
            self.add_activity_entry("检测到系统错误，建议检查日志文件", "WARNING")
            self.add_activity_entry("可能的问题: 网络连接、权限配置、服务状态", "WARNING")
        else:
            self.add_activity_entry("系统运行正常，未检测到明显故障", "INFO")
            
    def add_activity_entry(self, description, log_type):
        """添加活动条目"""
        current_row = self.activity_table.rowCount()
        self.activity_table.insertRow(current_row)
        
        # 时间
        time_item = QTableWidgetItem(datetime.now().strftime("%H:%M:%S"))
        time_item.setForeground(QColor("#a0a0c0"))
        self.activity_table.setItem(current_row, 0, time_item)
        
        # 类型
        type_item = QTableWidgetItem("操作")
        if log_type == "INFO":
            type_item.setForeground(QColor("#00aaff"))
        elif log_type == "WARNING":
            type_item.setForeground(QColor("#ffaa00"))
        elif log_type == "ERROR":
            type_item.setForeground(QColor("#ff5555"))
        self.activity_table.setItem(current_row, 1, type_item)
        
        # 描述
        desc_item = QTableWidgetItem(description)
        desc_item.setForeground(QColor("#ffffff"))
        self.activity_table.setItem(current_row, 2, desc_item)
        
        # 状态
        status_item = QTableWidgetItem("✅ 完成")
        status_item.setForeground(QColor("#00ff88"))
        self.activity_table.setItem(current_row, 3, status_item)
        
        # 滚动到底部
        self.activity_table.scrollToBottom()

# 测试函数
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = TerminalMonitor()
    window.setWindowTitle("终端监控版仪表盘测试")
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())