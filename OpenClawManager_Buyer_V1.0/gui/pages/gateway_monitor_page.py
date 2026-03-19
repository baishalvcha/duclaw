#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gateway监控窗口 - 提供Gateway状态监控和调试日志功能
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QTextEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QSplitter, QProgressBar,
    QComboBox, QLineEdit, QCheckBox, QToolBar, QStatusBar,
    QMainWindow, QDockWidget, QApplication, QFileDialog
)
from PySide6.QtCore import Qt, QTimer, QDateTime, QThread, pyqtSignal
from PySide6.QtGui import QTextCursor, QFont, QColor, QBrush
import subprocess
import threading
import time
import json
import os


class GatewayMonitorPage(QMainWindow):
    """Gateway监控窗口（独立窗口）"""
    
    def __init__(self):
        super().__init__()
        self.log_data = []  # 日志数据存储
        self.filtered_data = []  # 过滤后的日志数据
        self.is_monitoring = False  # 监控状态
        self.monitor_thread = None  # 监控线程
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("Gateway监控窗口 - 码泓mahong-openclaw管理器")
        self.setGeometry(100, 100, 1400, 800)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 顶部工具栏
        self.create_toolbar()
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪 (Ready)")
        
        # 创建分割器
        splitter = QSplitter(Qt.Vertical)
        
        # 上半部分：状态监控
        status_widget = self.create_status_widget()
        splitter.addWidget(status_widget)
        
        # 下半部分：日志监控
        log_widget = self.create_log_widget()
        splitter.addWidget(log_widget)
        
        # 设置分割器比例
        splitter.setSizes([300, 500])
        
        main_layout.addWidget(splitter)
        
        # 底部操作栏
        bottom_layout = self.create_bottom_toolbar()
        main_layout.addLayout(bottom_layout)
        
        # 启动定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(5000)  # 5秒更新一次状态
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QToolBar("工具栏")
        self.addToolBar(toolbar)
        
        # 开始监控按钮
        self.start_btn = QPushButton("开始监控")
        self.start_btn.clicked.connect(self.start_monitoring)
        toolbar.addWidget(self.start_btn)
        
        # 停止监控按钮
        self.stop_btn = QPushButton("停止监控")
        self.stop_btn.clicked.connect(self.stop_monitoring)
        self.stop_btn.setEnabled(False)
        toolbar.addWidget(self.stop_btn)
        
        toolbar.addSeparator()
        
        # 清空日志按钮
        clear_btn = QPushButton("清空日志")
        clear_btn.clicked.connect(self.clear_logs)
        toolbar.addWidget(clear_btn)
        
        # 导出日志按钮
        export_btn = QPushButton("导出日志")
        export_btn.clicked.connect(self.export_logs)
        toolbar.addWidget(export_btn)
        
        toolbar.addSeparator()
        
        # 重启Gateway按钮
        restart_btn = QPushButton("重启Gateway")
        restart_btn.clicked.connect(self.restart_gateway)
        toolbar.addWidget(restart_btn)
        
        # 停止Gateway按钮
        stop_gateway_btn = QPushButton("停止Gateway")
        stop_gateway_btn.clicked.connect(self.stop_gateway)
        toolbar.addWidget(stop_gateway_btn)
        
        # 启动Gateway按钮
        start_gateway_btn = QPushButton("启动Gateway")
        start_gateway_btn.clicked.connect(self.start_gateway)
        toolbar.addWidget(start_gateway_btn)
    
    def create_status_widget(self):
        """创建状态监控部件"""
        status_widget = QWidget()
        status_layout = QVBoxLayout(status_widget)
        
        # Gateway状态组
        gateway_group = QGroupBox("Gateway状态")
        gateway_layout = QVBoxLayout(gateway_group)
        
        # 状态显示行
        status_row = QHBoxLayout()
        status_label = QLabel("当前状态:")
        status_row.addWidget(status_label)
        
        self.status_label = QLabel("未知")
        self.status_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        status_row.addWidget(self.status_label)
        
        status_row.addStretch()
        gateway_layout.addLayout(status_row)
        
        # 状态详情表格
        self.status_table = QTableWidget()
        self.status_table.setColumnCount(3)
        self.status_table.setHorizontalHeaderLabels(["指标", "数值", "状态"])
        self.status_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.status_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # 初始化状态数据
        self.init_status_data()
        gateway_layout.addWidget(self.status_table)
        
        status_layout.addWidget(gateway_group)
        
        # 性能监控组
        perf_group = QGroupBox("性能监控")
        perf_layout = QVBoxLayout(perf_group)
        
        # CPU使用率
        cpu_layout = QHBoxLayout()
        cpu_label = QLabel("CPU使用率:")
        cpu_layout.addWidget(cpu_label)
        
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setRange(0, 100)
        self.cpu_progress.setValue(0)
        cpu_layout.addWidget(self.cpu_progress)
        
        self.cpu_label = QLabel("0%")
        cpu_layout.addWidget(self.cpu_label)
        cpu_layout.addStretch()
        perf_layout.addLayout(cpu_layout)
        
        # 内存使用率
        mem_layout = QHBoxLayout()
        mem_label = QLabel("内存使用率:")
        mem_layout.addWidget(mem_label)
        
        self.mem_progress = QProgressBar()
        self.mem_progress.setRange(0, 100)
        self.mem_progress.setValue(0)
        mem_layout.addWidget(self.mem_progress)
        
        self.mem_label = QLabel("0%")
        mem_layout.addWidget(self.mem_label)
        mem_layout.addStretch()
        perf_layout.addLayout(mem_layout)
        
        # 连接数
        conn_layout = QHBoxLayout()
        conn_label = QLabel("活动连接数:")
        conn_layout.addWidget(conn_label)
        
        self.conn_label = QLabel("0")
        self.conn_label.setStyleSheet("font-weight: bold;")
        conn_layout.addWidget(self.conn_label)
        conn_layout.addStretch()
        perf_layout.addLayout(conn_layout)
        
        status_layout.addWidget(perf_group)
        
        return status_widget
    
    def create_log_widget(self):
        """创建日志监控部件"""
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        
        # 日志过滤工具栏
        filter_toolbar = QHBoxLayout()
        
        # 日志级别过滤
        level_label = QLabel("日志级别:")
        filter_toolbar.addWidget(level_label)
        
        self.level_combo = QComboBox()
        self.level_combo.addItems(["全部", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.level_combo.currentTextChanged.connect(self.filter_logs)
        filter_toolbar.addWidget(self.level_combo)
        
        # 关键词过滤
        keyword_label = QLabel("关键词:")
        filter_toolbar.addWidget(keyword_label)
        
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("输入过滤关键词...")
        self.keyword_input.textChanged.connect(self.filter_logs)
        filter_toolbar.addWidget(self.keyword_input)
        
        # 自动滚动
        self.auto_scroll_check = QCheckBox("自动滚动")
        self.auto_scroll_check.setChecked(True)
        filter_toolbar.addWidget(self.auto_scroll_check)
        
        filter_toolbar.addStretch()
        log_layout.addLayout(filter_toolbar)
        
        # 日志显示区域
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 10))
        self.log_text.setLineWrapMode(QTextEdit.NoWrap)
        log_layout.addWidget(self.log_text)
        
        # 日志统计
        stats_layout = QHBoxLayout()
        self.total_logs_label = QLabel("总计: 0 条日志")
        self.filtered_logs_label = QLabel("显示: 0 条日志")
        self.last_update_label = QLabel("最后更新: --")
        
        stats_layout.addWidget(self.total_logs_label)
        stats_layout.addWidget(self.filtered_logs_label)
        stats_layout.addWidget(self.last_update_label)
        stats_layout.addStretch()
        
        log_layout.addLayout(stats_layout)
        
        return log_widget
    
    def create_bottom_toolbar(self):
        """创建底部工具栏"""
        bottom_layout = QHBoxLayout()
        
        # 复制选中日志按钮
        copy_btn = QPushButton("复制选中内容")
        copy_btn.clicked.connect(self.copy_selected_logs)
        bottom_layout.addWidget(copy_btn)
        
        # 查找日志按钮
        find_btn = QPushButton("查找...")
        find_btn.clicked.connect(self.find_in_logs)
        bottom_layout.addWidget(find_btn)
        
        # 时间范围选择
        time_label = QLabel("时间范围:")
        bottom_layout.addWidget(time_label)
        
        self.time_combo = QComboBox()
        self.time_combo.addItems(["全部", "最近1小时", "最近24小时", "最近7天"])
        self.time_combo.currentTextChanged.connect(self.filter_logs)
        bottom_layout.addWidget(self.time_combo)
        
        bottom_layout.addStretch()
        
        # 日志行数显示
        self.line_count_label = QLabel("行数: 0")
        bottom_layout.addWidget(self.line_count_label)
        
        return bottom_layout
    
    def init_status_data(self):
        """初始化状态数据"""
        status_data = [
            ["服务状态", "未知", "未知"],
            ["运行时间", "0秒", "未知"],
            ["版本信息", "未知", "未知"],
            ["配置文件", "未知", "未知"],
            ["日志文件", "未知", "未知"],
            ["错误计数", "0", "正常"],
            ["警告计数", "0", "正常"],
            ["最后错误", "无", "正常"]
        ]
        
        self.status_table.setRowCount(len(status_data))
        for i, (metric, value, status) in enumerate(status_data):
            # 指标
            metric_item = QTableWidgetItem(metric)
            self.status_table.setItem(i, 0, metric_item)
            
            # 数值
            value_item = QTableWidgetItem(value)
            self.status_table.setItem(i, 1, value_item)
            
            # 状态
            status_item = QTableWidgetItem(status)
            if status == "正常":
                status_item.setForeground(QBrush(QColor(40, 167, 69)))  # 绿色
            elif status == "警告":
                status_item.setForeground(QBrush(QColor(255, 193, 7)))  # 黄色
            elif status == "错误":
                status_item.setForeground(QBrush(QColor(220, 53, 69)))  # 红色
            else:
                status_item.setForeground(QBrush(QColor(108, 117, 125)))  # 灰色
            self.status_table.setItem(i, 2, status_item)
    
    def update_status(self):
        """更新Gateway状态"""
        try:
            # 执行openclaw gateway status命令
            result = subprocess.run(
                ["openclaw", "gateway", "status"],
                capture_output=True,
                text=True,
                shell=True
            )
            
            if result.returncode == 0:
                output = result.stdout
                if "running" in output.lower():
                    self.status_label.setText("运行中")
                    self.status_label.setStyleSheet("font-weight: bold; color: #28a745;")
                    
                    # 更新状态表格
                    self.update_status_table("运行中", "正常")
                else:
                    self.status_label.setText("已停止")
                    self.status_label.setStyleSheet("font-weight: bold; color: #dc3545;")
                    
                    # 更新状态表格
                    self.update_status_table("已停止", "错误")
            else:
                self.status_label.setText("未知")
                self.status_label.setStyleSheet("font-weight: bold; color: #666;")
                
                # 更新状态表格
                self.update_status_table("未知", "警告")
                
        except Exception as e:
            self.status_label.setText("检查失败")
            self.status_label.setStyleSheet("font-weight: bold; color: #dc3545;")
            self.status_bar.showMessage(f"状态检查失败: {str(e)}", 5000)
    
    def update_status_table(self, status, health):
        """更新状态表格"""
        # 更新服务状态
        self.status_table.item(0, 1).setText(status)
        
        # 更新状态颜色
        status_item = self.status_table.item(0, 2)
        status_item.setText(health)
        
        if health == "正常":
            status_item.setForeground(QBrush(QColor(40, 167, 69)))
        elif health == "警告":
            status_item.setForeground(QBrush(QColor(255, 193, 7)))
        else:
            status_item.setForeground(QBrush(QColor(220, 53, 69)))
    
    def start_monitoring(self):
        """开始监控"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            
            # 启动监控线程
            self.monitor_thread = MonitorThread()
            self.monitor_thread.log_received.connect(self.add_log_entry)
            self.monitor_thread.start()
            
            self.status_bar.showMessage("监控已启动", 3000)
            self.add_log_entry("INFO", "Gateway监控已启动")
    
    def stop_monitoring(self):
        """停止监控"""
        if self.is_monitoring:
            self.is_monitoring = False
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            
            # 停止监控线程
            if self.monitor_thread:
                self.monitor_thread.stop()
                self.monitor_thread = None
            
            self.status_bar.showMessage("监控已停止", 3000)
            self.add_log_entry("INFO", "Gateway监控已停止")
    
    def add_log_entry(self, level, message):
        """添加日志条目"""
        timestamp = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss.zzz")
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
        
        self.log_data.append(log_entry)
        
        # 应用过滤
        self.filter_logs()
        
        # 更新统计
        self.update_log_stats()
        
        # 自动滚动
        if self.auto_scroll_check.isChecked():
            self.log_text.moveCursor(QTextCursor.End)
    
    def filter_logs(self):
        """过滤日志"""
        level_filter = self.level_combo.currentText()
        keyword_filter = self.keyword_input.text().lower()
        
        self.filtered_data = []
        for entry in self.log_data:
            # 级别过滤
            if level_filter != "全部" and entry["level"] != level_filter:
                continue
            
            # 关键词过滤
            if keyword_filter and keyword_filter not in entry["message"].lower():
                continue
            
            self.filtered_data.append(entry)
        
        # 更新日志显示
        self.update_log_display()
    
    def update_log_display(self):
        """更新日志显示"""
        self.log_text.clear()
        
        for entry in self.filtered_data:
            timestamp = entry["timestamp"]
            level = entry["level"]
            message = entry["message"]
            
            # 设置颜色
            color = self.get_log_level_color(level)
            
            # 格式化日志行
            log_line = f"[{timestamp}] [{level}] {message}"
            
            # 添加到文本区域
            self.log_text.append(log_line)
            
            # 设置最后一行颜色
            cursor = self.log_text.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.select(QTextCursor.LineUnderCursor)
            
            format = cursor.charFormat()
            format.setForeground(QBrush(color))
            cursor.setCharFormat(format)
        
        # 更新行数
        self.line_count_label.setText(f"行数: {len(self.filtered_data)}")
    
    def get_log_level_color(self, level):
        """获取日志级别颜色"""
        colors = {
            "DEBUG": QColor(108, 117, 125),    # 灰色
            "INFO": QColor(0, 123, 255),       # 蓝色
            "WARNING": QColor(255, 193, 7),    # 黄色
            "ERROR": QColor(220, 53, 69),      # 红色
            "CRITICAL": QColor(220, 53, 69)    # 红色
        }
        return colors.get(level, QColor(0, 0, 0))
    
    def update_log_stats(self):
        """更新日志统计"""
        total_count = len(self.log_data)
        filtered_count = len(self.filtered_data)
        last_update = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        self.total_logs_label.setText(f"总计: {total_count} 条日志")
        self.filtered_logs_label.setText(f"显示: {filtered_count} 条日志")
        self.last_update_label.setText(f"最后更新: {last_update}")
    
    def clear_logs(self):
        """清空日志"""
        reply = QMessageBox.question(
            self,
            "确认清空",
            "确定要清空所有日志吗？此操作不可恢复。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.log_data.clear()
            self.filtered_data.clear()
            self.log_text.clear()
            self.update_log_stats()
            self.status_bar.showMessage("日志已清空", 3000)
    
    def export_logs(self):
        """导出日志"""
        if not self.log_data:
            QMessageBox.warning(self, "无日志", "没有日志可导出")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "导出日志",
            f"gateway_logs_{QDateTime.currentDateTime().toString('yyyyMMdd_HHmmss')}.txt",
            "文本文件 (*.txt);;所有文件 (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for entry in self.log_data:
                        f.write(f"[{entry['timestamp']}] [{entry['level']}] {entry['message']}\n")
                
                self.status_bar.showMessage(f"日志已导出到: {file_path}", 5000)
                QMessageBox.information(self, "导出成功", f"日志已成功导出到:\n{file_path}")
                
            except Exception as e:
                QMessageBox.warning(self, "导出失败", f"日志导出失败: {str(e)}")
    
    def copy_selected_logs(self):
        """复制选中日志"""
        selected_text = self.log_text.textCursor().selectedText()
        if selected_text:
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_text)
            self.status_bar.showMessage("选中内容已复制到剪贴板", 3000)
        else:
            QMessageBox.information(self, "无选中内容", "请先选择要复制的内容")
    
    def find_in_logs(self):
        """在日志中查找"""
        # 这里可以实现查找对话框
        QMessageBox.information(
            self,
            "查找功能",
            "查找功能正在开发中...\n\n"
            "当前可以使用关键词过滤功能进行搜索。"
        )
    
    def restart_gateway(self):
        """重启Gateway"""
        reply = QMessageBox.question(
            self,
            "确认重启",
            "确定要重启Gateway吗？这可能会中断正在进行的连接。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.add_log_entry("INFO", "正在重启Gateway...")
                
                # 停止Gateway
                subprocess.run(["openclaw", "gateway", "stop"], capture_output=True, shell=True)
                time.sleep(2)
                
                # 启动Gateway
                subprocess.run(["openclaw", "gateway", "start"], capture_output=True, shell=True)
                time.sleep(3)
                
                self.add_log_entry("INFO", "Gateway重启完成")
                self.update_status()
                
                QMessageBox.information(self, "重启完成", "Gateway已成功重启")
                
            except Exception as e:
                self.add_log_entry("ERROR", f"Gateway重启失败: {str(e)}")
                QMessageBox.warning(self, "重启失败", f"Gateway重启失败: {str(e)}")
    
    def stop_gateway(self):
        """停止Gateway"""
        reply = QMessageBox.question(
            self,
            "确认停止",
            "确定要停止Gateway吗？这将中断所有连接。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.add_log_entry("INFO", "正在停止Gateway...")
                subprocess.run(["openclaw", "gateway", "stop"], capture_output=True, shell=True)
                time.sleep(2)
                
                self.add_log_entry("INFO", "Gateway已停止")
                self.update_status()
                
                QMessageBox.information(self, "停止完成", "Gateway已成功停止")
                
            except Exception as e:
                self.add_log_entry("ERROR", f"Gateway停止失败: {str(e)}")
                QMessageBox.warning(self, "停止失败", f"Gateway停止失败: {str(e)}")
    
    def start_gateway(self):
        """启动Gateway"""
        try:
            self.add_log_entry("INFO", "正在启动Gateway...")
            subprocess.run(["openclaw", "gateway", "start"], capture_output=True, shell=True)
            time.sleep(3)
            
            self.add_log_entry("INFO", "Gateway已启动")
            self.update_status()
            
            QMessageBox.information(self, "启动完成", "Gateway已成功启动")
            
        except Exception as e:
            self.add_log_entry("ERROR", f"Gateway启动失败: {str(e)}")
            QMessageBox.warning(self, "启动失败", f"Gateway启动失败: {str(e)}")
    
    def load_settings(self):
        """加载设置"""
        # 这里可以加载用户设置
        pass
    
    def closeEvent(self, event):
        """关闭事件"""
        self.stop_monitoring()
        event.accept()


class MonitorThread(QThread):
    """监控线程"""
    
    log_received = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.running = True
    
    def run(self):
        """线程运行"""
        while self.running:
            try:
                # 模拟获取Gateway日志
                # 实际应该读取Gateway日志文件或API
                import random
                
                # 模拟日志级别
                levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
                level = random.choice(levels)
                
                # 模拟日志消息
                messages = [
                    "Gateway运行正常",
                    "处理新的连接请求",
                    "心跳检测通过",
                    "内存使用率正常",
                    "CPU使用率正常",
                    "连接数: 5",
                    "日志轮转完成",
                    "配置已重新加载"
                ]
                
                if level == "ERROR":
                    messages = [
                        "连接超时",
                        "内存不足警告",
                        "配置文件错误",
                        "网络连接失败"
                    ]
                
                message = random.choice(messages)
                
                # 发送日志信号
                self.log_received.emit(level, message)
                
                # 等待一段时间
                time.sleep(random.uniform(0.5, 2.0))
                
            except Exception as e:
                self.log_received.emit("ERROR", f"监控线程错误: {str(e)}")
                time.sleep(5)
    
    def stop(self):
        """停止线程"""
        self.running = False
        self.wait()


# 测试代码
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = GatewayMonitorPage()
    window.show()
    sys.exit(app.exec())
