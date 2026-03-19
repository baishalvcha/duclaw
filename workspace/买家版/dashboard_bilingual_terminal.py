#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双语终端监控版仪表盘 - 左边原文，右边翻译/分析
"""

import sys
import random
from datetime import datetime, timedelta
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QPushButton, QLabel, QTableWidget,
                              QTableWidgetItem, QHeaderView, QFrame, QTextEdit,
                              QSplitter, QComboBox, QLineEdit, QGridLayout,
                              QFileDialog)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QTextCursor

class BilingualTerminalMonitor(QWidget):
    """双语终端监控界面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.terminal_output = []
        self.analysis_output = []
        self.is_executing = False  # 执行状态标志
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
        title_label.setStyleSheet("color: #ffffff;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
        
        # 创建水平分割器
        main_splitter = QSplitter(Qt.Horizontal)
        # 隐藏分割器手柄（去掉白色线条）
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: transparent;
                width: 0px;
                height: 0px;
            }
            QSplitter::handle:horizontal {
                width: 0px;
            }
            QSplitter::handle:vertical {
                height: 0px;
            }
        """)
        
        # 左边：终端原文面板
        left_panel = self.create_terminal_panel("终端原文", True)
        main_splitter.addWidget(left_panel)
        
        # 右边：翻译/分析面板
        right_panel = self.create_analysis_panel("翻译/分析", False)
        main_splitter.addWidget(right_panel)
        
        # 设置分割器比例
        main_splitter.setSizes([500, 500])
        
        layout.addWidget(main_splitter)
        
        # 创建垂直分割器（下半部分）
        bottom_splitter = QSplitter(Qt.Vertical)
        # 隐藏分割器手柄（去掉白色线条）
        bottom_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: transparent;
                width: 0px;
                height: 0px;
            }
            QSplitter::handle:horizontal {
                width: 0px;
            }
            QSplitter::handle:vertical {
                height: 0px;
            }
        """)
        
        # 命令控制面板
        control_panel = self.create_control_panel()
        bottom_splitter.addWidget(control_panel)
        
        # 活动表格面板
        activity_panel = self.create_activity_panel()
        bottom_splitter.addWidget(activity_panel)
        
        # 设置分割器比例
        bottom_splitter.setSizes([150, 250])
        
        layout.addWidget(bottom_splitter)
        

        
    def create_terminal_panel(self, title, is_left=True):
        """创建终端原文面板"""
        panel = QGroupBox(title)
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
                color: #ffffff;
            }
        """)
        
        layout = QVBoxLayout(panel)
        
        # 终端输出显示
        if is_left:
            self.terminal_text = QTextEdit()
            self.terminal_text.setStyleSheet("""
                QTextEdit {
                    background-color: #0f0f1a;
                    color: #ffffff;
                    border: 1px solid #2d2d4d;
                    border-radius: 4px;
                    font-family: 'Consolas', 'Monaco', monospace;
                    font-size: 11px;
                }
            """)
            self.terminal_text.setReadOnly(True)
            layout.addWidget(self.terminal_text)
        else:
            self.analysis_text = QTextEdit()
            self.analysis_text.setStyleSheet("""
                QTextEdit {
                    background-color: #0f0f1a;
                    color: #ffffff;
                    border: 1px solid #2d2d4d;
                    border-radius: 4px;
                    font-family: 'Microsoft YaHei', 'SimHei', sans-serif;
                    font-size: 12px;
                }
            """)
            self.analysis_text.setReadOnly(True)
            layout.addWidget(self.analysis_text)
        
        return panel
        
    def create_analysis_panel(self, title, is_left=False):
        """创建翻译/分析面板"""
        return self.create_terminal_panel(title, False)
        
    def create_control_panel(self):
        """创建命令控制面板"""
        panel = QGroupBox("命令控制")
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
                color: #ffffff;
            }
        """)
        
        # 创建垂直布局，分为上下两部分
        main_layout = QVBoxLayout(panel)
        
        # ========== 第一部分：命令控制区域 ==========
        command_frame = QFrame()
        command_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a2e;
                border: 1px solid #2d2d4d;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        
        command_layout = QHBoxLayout(command_frame)
        
        # 中文指令选择（最左边）- 去掉标签，设置默认值
        
        self.chinese_command_combo = QComboBox()
        self.chinese_command_combo.addItems([
            "请选择中文指令",  # 默认值
            "查看OpenClaw实时日志",
            "运行OpenClaw诊断工具",
            "查看OpenClaw系统状态",
            "查看Gateway服务状态",
            "查看系统服务状态",
            "实时监控日志文件",
            "网络连通性测试",
            "查看网络连接状态"
        ])
        self.chinese_command_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 300px;
            }
        """)
        self.chinese_command_combo.setCurrentIndex(0)  # 设置为默认值
        self.chinese_command_combo.currentIndexChanged.connect(self.on_chinese_command_changed)
        command_layout.addWidget(self.chinese_command_combo)
        
        # 英文指令选择（挨着中文命令）- 去掉标签，设置默认值
        
        self.command_combo = QComboBox()
        self.command_combo.addItems([
            "请选择英文指令",  # 默认值
            "openclaw logs --follow",
            "openclaw doctor",
            "openclaw status",
            "openclaw gateway status",
            "systemctl status openclaw",
            "tail -f ~/.openclaw/logs/gateway.log",
            "ping -c 4 8.8.8.8",
            "netstat -tulpn | grep openclaw"
        ])
        self.command_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                border-radius: 4px;
                padding: 5px;
                min-width: 300px;
            }
        """)
        self.command_combo.setCurrentIndex(0)  # 设置为默认值
        self.command_combo.currentIndexChanged.connect(self.on_english_command_changed)
        command_layout.addWidget(self.command_combo)
        
        # 自定义命令输入（最大宽度）- 去掉标签，修改提示信息，增加宽度
        
        self.custom_command = QLineEdit()
        self.custom_command.setPlaceholderText("请输入openclaw命令行")
        self.custom_command.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        command_layout.addWidget(self.custom_command, 1)  # 拉伸因子为1，最大宽度
        
        # 执行按钮
        self.execute_btn = QPushButton("🚀 执行")
        self.execute_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffffff;
                color: #0f0f1a;
            }
        """)
        self.execute_btn.clicked.connect(self.execute_command)
        command_layout.addWidget(self.execute_btn)
        
        # 停止按钮
        self.stop_btn = QPushButton("⏹️ 停止")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffffff;
                color: #0f0f1a;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_terminal_monitor)
        self.stop_btn.setEnabled(False)
        command_layout.addWidget(self.stop_btn)
        
        main_layout.addWidget(command_frame)
        
        # ========== 第二部分：日志操作区域 ==========
        log_frame = QFrame()
        log_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a2e;
                border: 1px solid #2d2d4d;
                border-radius: 6px;
                padding: 10px;
                margin-top: 10px;
            }
        """)
        
        log_layout = QHBoxLayout(log_frame)
        
        # 左侧占位符，让复制按钮与中文命令左对齐
        log_layout.addStretch(1)
        
        # 复制终端原文按钮（与中文命令左对齐）
        copy_terminal_btn = QPushButton("📋 复制终端原文")
        copy_terminal_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
                min-width: 300px;
            }
            QPushButton:hover {
                background-color: #ffffff;
                color: #0f0f1a;
            }
        """)
        copy_terminal_btn.clicked.connect(self.copy_terminal_only)
        log_layout.addWidget(copy_terminal_btn)
        
        # 导出原文按钮
        export_btn = QPushButton("📤 导出原文")
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
                min-width: 300px;
            }
            QPushButton:hover {
                background-color: #ffffff;
                color: #0f0f1a;
            }
        """)
        export_btn.clicked.connect(self.export_terminal_text)
        log_layout.addWidget(export_btn)
        
        # 清空全部按钮
        self.clear_all_btn = QPushButton("🗑️ 清空全部")
        self.clear_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
                min-width: 300px;
            }
            QPushButton:hover {
                background-color: #ffffff;
                color: #0f0f1a;
            }
        """)
        self.clear_all_btn.clicked.connect(self.clear_all_output)
        log_layout.addWidget(self.clear_all_btn)
        
        # 导出/保存日志按钮（与上面"停止"按钮右对齐）
        export_save_btn = QPushButton("💾 导出/保存日志")
        export_save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
                min-width: 300px;
            }
            QPushButton:hover {
                background-color: #ffffff;
                color: #0f0f1a;
            }
        """)
        export_save_btn.clicked.connect(self.export_save_logs)
        log_layout.addWidget(export_save_btn)
        
        # 右侧占位符，让导出/保存日志按钮与停止按钮右对齐
        log_layout.addStretch(1)
        
        main_layout.addWidget(log_frame)
        
        # 提示信息（已移除）
        
        return panel
        
    def create_activity_panel(self):
        """创建活动表格面板"""
        panel = QGroupBox("最新活动")
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
                color: #ffffff;
            }
        """)
        
        layout = QVBoxLayout(panel)
        
        # 分析故障按钮（仅保留此按钮）
        analyze_btn = QPushButton("🔍 分析故障")
        analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d4d;
                color: #ffffff;
                border: 1px solid #3a3a5a;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #ffffff;
                color: #0f0f1a;
            }
        """)
        analyze_btn.clicked.connect(self.analyze_faults)
        layout.addWidget(analyze_btn)
        
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
                color: #ffffff;
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
        self.activity_table.verticalHeader().setVisible(False)  # 隐藏行号
        
        # 设置列宽（描述列最宽，状态列最小）
        self.activity_table.setColumnWidth(0, 80)   # 时间（更小）
        self.activity_table.setColumnWidth(1, 50)   # 类型（更小）
        self.activity_table.setColumnWidth(2, 600)  # 描述（最宽，大幅加宽）
        self.activity_table.setColumnWidth(3, 30)   # 状态（最小，大幅缩小）
        
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
                type_item.setForeground(QColor("#3a3a5a"))
            elif log["type"] == "错误":
                type_item.setForeground(QColor("#3a3a5a"))
            elif log["type"] == "警告":
                type_item.setForeground(QColor("#3a3a5a"))
            self.activity_table.setItem(i, 1, type_item)
            
            # 描述
            desc_item = QTableWidgetItem(log["description"])
            desc_item.setForeground(QColor("#ffffff"))
            self.activity_table.setItem(i, 2, desc_item)
            
            # 状态
            status_item = QTableWidgetItem(log["status"])
            if "成功" in log["status"]:
                status_item.setForeground(QColor("#3a3a5a"))
            elif "警告" in log["status"]:
                status_item.setForeground(QColor("#3a3a5a"))
            elif "失败" in log["status"]:
                status_item.setForeground(QColor("#3a3a5a"))
            self.activity_table.setItem(i, 3, status_item)
            

        
    def on_chinese_command_changed(self, index):
        """中文指令改变时，同步英文指令"""
        # 防止递归调用
        if hasattr(self, '_updating_commands'):
            return
            
        self._updating_commands = True
        
        # 中英文指令对应关系
        chinese_to_english = {
            0: 0,  # 查看OpenClaw实时日志 -> openclaw logs --follow
            1: 1,  # 运行OpenClaw诊断工具 -> openclaw doctor
            2: 2,  # 查看OpenClaw系统状态 -> openclaw status
            3: 3,  # 查看Gateway服务状态 -> openclaw gateway status
            4: 4,  # 查看系统服务状态 -> systemctl status openclaw
            5: 5,  # 实时监控日志文件 -> tail -f ~/.openclaw/logs/gateway.log
            6: 6,  # 网络连通性测试 -> ping -c 4 8.8.8.8
            7: 7   # 查看网络连接状态 -> netstat -tulpn | grep openclaw
        }
        
        if index in chinese_to_english:
            english_index = chinese_to_english[index]
            self.command_combo.setCurrentIndex(english_index)
            
        delattr(self, '_updating_commands')
        
    def on_english_command_changed(self, index):
        """英文指令改变时，同步中文指令"""
        # 防止递归调用
        if hasattr(self, '_updating_commands'):
            return
            
        self._updating_commands = True
        
        # 英文到中文指令对应关系
        english_to_chinese = {
            0: 0,  # openclaw logs --follow -> 查看OpenClaw实时日志
            1: 1,  # openclaw doctor -> 运行OpenClaw诊断工具
            2: 2,  # openclaw status -> 查看OpenClaw系统状态
            3: 3,  # openclaw gateway status -> 查看Gateway服务状态
            4: 4,  # systemctl status openclaw -> 查看系统服务状态
            5: 5,  # tail -f ~/.openclaw/logs/gateway.log -> 实时监控日志文件
            6: 6,  # ping -c 4 8.8.8.8 -> 网络连通性测试
            7: 7   # netstat -tulpn | grep openclaw -> 查看网络连接状态
        }
        
        if index in english_to_chinese:
            chinese_index = english_to_chinese[index]
            self.chinese_command_combo.setCurrentIndex(chinese_index)
            
        delattr(self, '_updating_commands')
        
    def start_system_monitoring(self):
        """开始系统监控"""
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_system_status)
        self.monitor_timer.start(5000)  # 每5秒更新一次系统状态
        
    def get_current_time(self):
        """获取当前时间"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def update_system_status(self):
        """更新系统状态"""
        # 模拟系统状态更新
        current_time = self.get_current_time()
        # 如果update_label不存在，先创建它
        if not hasattr(self, 'update_label'):
            # 创建一个简单的QLabel用于显示更新时间
            self.update_label = QLabel(f"最后更新: {current_time}")
            self.update_label.setStyleSheet("color: #a0a0c0; font-size: 12px;")
            # 添加到界面中（这里需要根据实际布局调整）
            # 暂时只创建对象，不添加到布局
        else:
            self.update_label.setText(f"最后更新: {current_time}")
        print(f"系统状态更新: {current_time}")  # 调试输出
        

        
    def start_terminal_monitor(self):
        """启动终端监控（兼容旧函数）"""
        self.execute_command()
        
    def stop_terminal_monitor(self):
        """停止终端监控（关闭调试终端窗口）"""
        # 停止实时监控定时器
        if hasattr(self, 'monitoring_timer'):
            self.monitoring_timer.stop()
            delattr(self, 'monitoring_timer')
            
        self.add_activity_entry("停止监控", "INFO")
        
        # 添加停止提示
        self.append_terminal_output("⏹️ 监控已停止 - 调试终端窗口关闭")
        self.append_analysis_output("⏹️ 监控已停止 - 调试终端窗口关闭")
        
        self.execute_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.clear_all_btn.setEnabled(True)  # 启用清空全部按钮
        self.is_executing = False  # 重置执行状态标志
        
    def simulate_terminal_output(self, command):
        """模拟终端输出（用于非实时命令）"""
        # 根据命令类型生成不同的模拟输出
        if "doctor" in command:
            # 左边：英文原文
            self.append_terminal_output("🩺 Running OpenClaw diagnostic tool...")
            self.append_terminal_output("✅ Check 1: Gateway service status - OK")
            self.append_terminal_output("✅ Check 2: Configuration file integrity - OK")
            self.append_terminal_output("✅ Check 3: Network connectivity test - OK")
            self.append_terminal_output("✅ Check 4: Model availability - OK")
            self.append_terminal_output("✅ Check 5: Permission settings - OK")
            self.append_terminal_output("🎉 All diagnostic checks passed! System is healthy")
            
            # 右边：中文翻译/分析
            self.append_analysis_output("🩺 运行 OpenClaw 诊断工具...")
            self.append_analysis_output("✅ 检查 1: Gateway 服务状态 - 正常")
            self.append_analysis_output("✅ 检查 2: 配置文件完整性 - 正常")
            self.append_analysis_output("✅ 检查 3: 网络连接测试 - 正常")
            self.append_analysis_output("✅ 检查 4: 模型可用性 - 正常")
            self.append_analysis_output("✅ 检查 5: 权限设置 - 正常")
            self.append_analysis_output("🎉 所有诊断检查通过！系统健康")
            
        elif "status" in command:
            # 左边：英文原文
            self.append_terminal_output("📊 OpenClaw system status:")
            self.append_terminal_output("  ├─ Gateway: 🟢 Running")
            self.append_terminal_output("  ├─ QQ Bot: 🟢 Connected")
            self.append_terminal_output("  ├─ Feishu: 🟡 Configuring")
            self.append_terminal_output("  ├─ WeChat: 🔴 Not configured")
            self.append_terminal_output("  ├─ Models: 🟢 Available (5)")
            self.append_terminal_output("  └─ Memory: 🟡 65% usage")
            
            # 右边：中文翻译/分析
            self.append_analysis_output("📊 OpenClaw 系统状态:")
            self.append_analysis_output("  ├─ Gateway: 🟢 运行中")
            self.append_analysis_output("  ├─ QQ Bot: 🟢 已连接")
            self.append_analysis_output("  ├─ 飞书: 🟡 配置中")
            self.append_analysis_output("  ├─ 微信: 🔴 未配置")
            self.append_analysis_output("  ├─ 模型: 🟢 可用 (5个)")
            self.append_analysis_output("  └─ 内存: 🟡 65% 使用率")
            
        else:
            # 左边：英文原文
            self.append_terminal_output(f"🚀 Executing command: {command}")
            self.append_terminal_output("📝 Command output simulation...")
            self.append_terminal_output("✅ Command executed successfully")
            self.append_terminal_output("📊 Output results displayed")
            
            # 右边：中文翻译/分析
            self.append_analysis_output(f"🚀 执行命令: {command}")
            self.append_analysis_output("📝 命令输出模拟...")
            self.append_analysis_output("✅ 命令执行成功")
            self.append_analysis_output("📊 输出结果已显示")
            
    def append_terminal_output(self, text):
        """添加终端输出（左边）"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_text = f"[{timestamp}] {text}"
        
        self.terminal_text.append(formatted_text)
        
        # 滚动到底部
        cursor = self.terminal_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.terminal_text.setTextCursor(cursor)
        
    def append_analysis_output(self, text):
        """添加分析输出（右边）"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_text = f"[{timestamp}] {text}"
        
        self.analysis_text.append(formatted_text)
        
        # 滚动到底部
        cursor = self.analysis_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.analysis_text.setTextCursor(cursor)
        
    def copy_terminal_only(self):
        """仅复制终端原文"""
        import pyperclip
        
        try:
            text = self.terminal_text.toPlainText()
            if text:
                pyperclip.copy(text)
                self.add_activity_entry("终端原文已复制到剪贴板", "INFO")
            else:
                self.add_activity_entry("终端原文为空", "WARNING")
        except ImportError:
            self.add_activity_entry("需要安装pyperclip库: pip install pyperclip", "ERROR")
        except Exception as e:
            self.add_activity_entry(f"复制失败: {str(e)}", "ERROR")
            
    def export_terminal_text(self):
        """导出终端原文到文件（带文件夹选择）"""
        text = self.terminal_text.toPlainText()
        if text:
            # 弹出文件夹选择对话框
            folder_path = QFileDialog.getExistingDirectory(
                self,
                "选择保存文件夹",
                "",
                QFileDialog.ShowDirsOnly
            )
            
            if folder_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"terminal_original_{timestamp}.txt"
                file_path = f"{folder_path}/{filename}"
                
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    self.add_activity_entry(f"终端原文已导出到: {file_path}", "INFO")
                except Exception as e:
                    self.add_activity_entry(f"导出失败: {str(e)}", "ERROR")
            else:
                self.add_activity_entry("导出已取消", "WARNING")
        else:
            self.add_activity_entry("终端原文为空", "WARNING")
            
    def export_save_logs(self):
        """导出/保存日志（合并功能）"""
        text = self.terminal_text.toPlainText()
        if text:
            # 弹出文件保存对话框
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"openclaw_logs_{timestamp}.txt"
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "保存终端日志",
                default_filename,
                "文本文件 (*.txt);;所有文件 (*.*)"
            )
            
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    self.add_activity_entry(f"日志已保存到: {file_path}", "INFO")
                except Exception as e:
                    self.add_activity_entry(f"保存失败: {str(e)}", "ERROR")
            else:
                self.add_activity_entry("保存已取消", "WARNING")
        else:
            self.add_activity_entry("终端原文为空", "WARNING")
            
    def clear_all_output(self):
        """清空全部输出"""
        self.terminal_text.clear()
        self.analysis_text.clear()
        self.add_activity_entry("全部输出已清空", "INFO")
        
    def execute_command(self):
        """执行命令（实现实时监控）"""
        # 检查是否正在执行（按钮应该是灰色的，但这里作为安全检查）
        if self.is_executing:
            # 不弹窗，直接返回
            return
        
        # 验证输入
        chinese_selected = self.chinese_command_combo.currentText()
        english_selected = self.command_combo.currentText()
        custom_command = self.custom_command.text()
        
        # 检查是否选择了默认值或空白值
        if (chinese_selected == "请选择中文指令" or english_selected == "请选择英文指令") and not custom_command:
            # 弹出提示框
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "输入提示", "请选择中文指令或选择英文指令、或手动输入openclaw命令")
            return
        
        # 优先使用自定义命令
        if custom_command:
            command = custom_command
            chinese_command = "自定义命令"
        else:
            # 使用英文命令
            command = english_selected
            chinese_command = chinese_selected
            
        # 获取对应的中文描述
        if chinese_command == "请选择中文指令":
            chinese_command = "未选择指令"
        
        self.add_activity_entry(f"执行命令: {chinese_command}", "INFO")
        
        # 清空现有输出
        self.terminal_text.clear()
        self.analysis_text.clear()
        
        # 开始实时监控
        self.start_real_time_monitoring(command)
        
        self.execute_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.clear_all_btn.setEnabled(False)  # 禁用清空全部按钮
        self.is_executing = True  # 设置执行状态标志
        
    def start_real_time_monitoring(self, command):
        """开始实时监控"""
        # 停止之前的定时器（如果存在）
        if hasattr(self, 'monitoring_timer'):
            self.monitoring_timer.stop()
            
        # 根据命令类型生成不同的模拟输出
        if "logs --follow" in command or "tail -f" in command:
            # 实时日志监控模式
            self.append_terminal_output("🔍 开始实时监控 OpenClaw 日志...")
            self.append_analysis_output("🔍 开始实时监控 OpenClaw 日志...")
            
            # 创建定时器模拟实时输出
            self.monitoring_timer = QTimer()
            self.monitoring_timer.timeout.connect(lambda: self.append_real_time_logs(command))
            self.monitoring_timer.start(1000)  # 每秒更新一次
            
        else:
            # 普通命令执行模式
            self.simulate_terminal_output(command)
            # 普通命令执行完毕后，延迟1秒自动恢复按钮状态
            # 让用户有时间看到命令执行完毕的提示
            QTimer.singleShot(1000, self.restore_button_state)
            
    def restore_button_state(self):
        """恢复按钮状态（用于普通命令执行完毕后）"""
        # 清空上一个命令的执行结果，避免无效信息
        self.terminal_text.clear()
        self.analysis_text.clear()
        
        # 恢复按钮状态
        self.execute_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.clear_all_btn.setEnabled(True)
        self.is_executing = False
        
        # 添加活动记录，让用户知道可以执行下一个命令了
        self.add_activity_entry("命令执行完毕，终端已清空，可以执行下一个命令", "INFO")
            
    def append_real_time_logs(self, command):
        """追加实时日志（模拟）"""
        import random
        from datetime import datetime
        
        # 生成随机的日志条目
        log_types = ["INFO", "DEBUG", "WARNING", "ERROR"]
        log_type = random.choice(log_types)
        
        # 生成时间戳
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # 生成日志内容
        log_messages = [
            f"Gateway service heartbeat",
            f"QQ Bot message received",
            f"Model inference completed",
            f"Memory usage: {random.randint(50, 80)}%",
            f"Network latency: {random.randint(10, 100)}ms",
            f"Database query executed",
            f"User session updated",
            f"Cache refreshed",
            f"API request processed",
            f"System check passed"
        ]
        
        log_message = random.choice(log_messages)
        
        # 左边：英文原文
        english_log = f"[{timestamp}] [{log_type}] {log_message}"
        self.append_terminal_output(english_log)
        
        # 右边：中文翻译
        chinese_translations = {
            "Gateway service heartbeat": "Gateway 服务心跳",
            "QQ Bot message received": "QQ Bot 收到消息",
            "Model inference completed": "模型推理完成",
            "Memory usage": "内存使用",
            "Network latency": "网络延迟",
            "Database query executed": "数据库查询执行",
            "User session updated": "用户会话更新",
            "Cache refreshed": "缓存刷新",
            "API request processed": "API 请求处理",
            "System check passed": "系统检查通过"
        }
        
        chinese_message = chinese_translations.get(log_message.split(":")[0], log_message)
        chinese_log = f"[{timestamp}] [{log_type}] {chinese_message}"
        
        if "Memory usage" in log_message:
            chinese_log += f": {log_message.split(': ')[1]}"
        elif "Network latency" in log_message:
            chinese_log += f": {log_message.split(': ')[1]}"
            
        self.append_analysis_output(chinese_log)
        
    def analyze_faults(self):
        """分析故障"""
        # 模拟故障分析
        self.add_activity_entry("开始分析系统故障...", "INFO")
        
        # 检查终端输出中的错误
        terminal_text = self.terminal_text.toPlainText()
        
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
            type_item.setForeground(QColor("#3a3a5a"))
        elif log_type == "ERROR":
            type_item.setForeground(QColor("#3a3a5a"))
        self.activity_table.setItem(current_row, 1, type_item)
        
        # 描述
        desc_item = QTableWidgetItem(description)
        desc_item.setForeground(QColor("#ffffff"))
        self.activity_table.setItem(current_row, 2, desc_item)
        
        # 状态
        status_item = QTableWidgetItem("✅ 完成")
        status_item.setForeground(QColor("#3a3a5a"))
        self.activity_table.setItem(current_row, 3, status_item)
        
        # 滚动到底部
        self.activity_table.scrollToBottom()

# 测试函数
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = BilingualTerminalMonitor()
    window.setWindowTitle("终端监控版仪表盘测试")
    window.resize(1400, 900)
    window.show()
    sys.exit(app.exec())