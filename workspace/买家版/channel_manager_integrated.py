#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成版通道管理 - 包含调试日志功能
"""

import sys
import json
from datetime import datetime
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QTableWidget, QTableWidgetItem, QHeaderView,
                              QPushButton, QLabel, QLineEdit, QComboBox,
                              QTextEdit, QMenu, QMessageBox, QFileDialog,
                              QSplitter, QFrame)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QFont, QColor

class ChannelManagerIntegrated(QWidget):
    """集成版通道管理器（带调试日志）"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.channels = []
        self.selected_channels = set()
        self.debug_logs = []
        self.load_sample_data()
        self.init_ui()
        
    def load_sample_data(self):
        """加载示例数据"""
        self.channels = [
            {
                "id": "qqbot_001",
                "app_id": "QQBOT001",
                "account_id": "user_001",
                "name": "QQ Bot - 客服",
                "platform": "QQ",
                "platform_name": "QQ Bot平台",
                "role": "客服",
                "status": "运行中",
                "config_status": "已配置",
                "created_at": "2026-03-18 10:00:00"
            },
            {
                "id": "feishu_001",
                "app_id": "FEISHU001",
                "account_id": "user_002",
                "name": "飞书 - 内部沟通",
                "platform": "飞书",
                "platform_name": "飞书开放平台",
                "role": "内部沟通",
                "status": "运行中",
                "config_status": "已配置",
                "created_at": "2026-03-18 11:00:00"
            },
            {
                "id": "wechat_001",
                "app_id": "WECHAT001",
                "account_id": "user_003",
                "name": "微信 - 客户服务",
                "platform": "微信",
                "platform_name": "微信公众平台",
                "role": "客户服务",
                "status": "配置中",
                "config_status": "部分配置",
                "created_at": "2026-03-18 12:00:00"
            },
            {
                "id": "dingtalk_001",
                "app_id": "DINGTALK001",
                "account_id": "user_004",
                "name": "钉钉 - 工作通知",
                "platform": "钉钉",
                "platform_name": "钉钉开放平台",
                "role": "工作通知",
                "status": "未配置",
                "config_status": "未配置",
                "created_at": "2026-03-18 13:00:00"
            },
            {
                "id": "qqbot_002",
                "app_id": "QQBOT002",
                "account_id": "user_005",
                "name": "QQ Bot - 营销",
                "platform": "QQ",
                "platform_name": "QQ Bot营销平台",
                "role": "营销",
                "status": "运行中",
                "config_status": "已配置",
                "created_at": "2026-03-18 14:00:00"
            },
            {
                "id": "feishu_002",
                "app_id": "FEISHU002",
                "account_id": "user_006",
                "name": "飞书 - 项目管理",
                "platform": "飞书",
                "platform_name": "飞书项目管理",
                "role": "项目管理",
                "status": "运行中",
                "config_status": "已配置",
                "created_at": "2026-03-18 15:00:00"
            }
        ]
        
    def filter_non_actual_channels(self, channels):
        """过滤非实际使用的通道"""
        filtered = []
        for channel in channels:
            if channel["id"] not in ["default", "main"]:
                filtered.append(channel)
        return filtered
        
    def search_channels(self, search_type, keyword):
        """搜索通道"""
        if not keyword:
            return self.filter_non_actual_channels(self.channels)
            
        filtered = []
        keyword_lower = keyword.lower()
        
        for channel in self.channels:
            # 过滤非实际使用的通道
            if channel["id"] in ["default", "main"]:
                continue
                
            if search_type == "app_id":
                if keyword_lower in channel["app_id"].lower():
                    filtered.append(channel)
            elif search_type == "account_id":
                if keyword_lower in channel["account_id"].lower():
                    filtered.append(channel)
            elif search_type == "platform_name":
                if keyword_lower in channel["platform_name"].lower():
                    filtered.append(channel)
            elif search_type == "role":
                if keyword_lower in channel["role"].lower():
                    filtered.append(channel)
            elif search_type == "status":
                if keyword_lower in channel["status"].lower():
                    filtered.append(channel)
            elif search_type == "all":
                # 在所有字段中搜索
                search_fields = [
                    channel["id"], channel["app_id"], channel["account_id"],
                    channel["name"], channel["platform"], channel["platform_name"],
                    channel["role"], channel["status"], channel["config_status"]
                ]
                if any(keyword_lower in str(field).lower() for field in search_fields):
                    filtered.append(channel)
                    
        return filtered
        
    def add_debug_log(self, message, level="INFO"):
        """添加调试日志"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.debug_logs.append(log_entry)
        
        # 更新日志显示（最多保留100条）
        if len(self.debug_logs) > 100:
            self.debug_logs = self.debug_logs[-100:]
            
        self.update_debug_log_display()
        
    def update_debug_log_display(self):
        """更新调试日志显示"""
        self.debug_log_text.setPlainText("\n".join(self.debug_logs))
        # 滚动到底部
        scrollbar = self.debug_log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 创建分割器
        splitter = QSplitter(Qt.Vertical)
        
        # 上半部分：通道管理
        top_panel = QWidget()
        top_layout = QVBoxLayout(top_panel)
        
        # 搜索区域
        search_group = QGroupBox("通道搜索")
        search_layout = QVBoxLayout()
        
        # 搜索条件选择
        condition_layout = QHBoxLayout()
        condition_layout.addWidget(QLabel("搜索条件:"))
        
        self.search_type_combo = QComboBox()
        self.search_type_combo.addItems([
            "App ID", 
            "账户ID", 
            "平台名称",
            "角色", 
            "状态",
            "全部字段"
        ])
        condition_layout.addWidget(self.search_type_combo)
        
        # 搜索输入框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入搜索关键词...")
        self.search_input.textChanged.connect(self.on_search_changed)
        condition_layout.addWidget(self.search_input)
        
        # 搜索按钮
        search_btn = QPushButton("🔍 搜索")
        search_btn.clicked.connect(self.search_channels_action)
        condition_layout.addWidget(search_btn)
        
        # 清空按钮
        clear_btn = QPushButton("🗑️ 清空")
        clear_btn.clicked.connect(self.clear_search)
        condition_layout.addWidget(clear_btn)
        
        condition_layout.addStretch()
        search_layout.addLayout(condition_layout)
        
        search_group.setLayout(search_layout)
        top_layout.addWidget(search_group)
        
        # 通道列表区域
        list_group = QGroupBox("通道列表")
        list_layout = QVBoxLayout()
        
        # 创建表格
        self.channel_table = QTableWidget()
        self.channel_table.setColumnCount(9)
        self.channel_table.setHorizontalHeaderLabels([
            "选择", "ID", "App ID", "账户ID", "名称", "平台", "平台名称", "角色", "状态"
        ])
        
        # 设置列宽
        self.channel_table.setColumnWidth(0, 50)   # 选择
        self.channel_table.setColumnWidth(1, 100)  # ID
        self.channel_table.setColumnWidth(2, 100)  # App ID
        self.channel_table.setColumnWidth(3, 100)  # 账户ID
        self.channel_table.setColumnWidth(4, 150)  # 名称
        self.channel_table.setColumnWidth(5, 80)   # 平台
        self.channel_table.setColumnWidth(6, 120)  # 平台名称
        self.channel_table.setColumnWidth(7, 100)  # 角色
        self.channel_table.setColumnWidth(8, 80)   # 状态
        
        self.channel_table.horizontalHeader().setStretchLastSection(True)
        
        # 启用多选
        self.channel_table.setSelectionMode(QTableWidget.MultiSelection)
        self.channel_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # 连接选择事件
        self.channel_table.itemClicked.connect(self.on_item_clicked)
        
        list_layout.addWidget(self.channel_table)
        
        # 选择操作提示
        select_hint = QLabel("选择提示: Ctrl+单击（点选） | Shift+单击（块选） | 单击（选中/取消选中）")
        select_hint.setStyleSheet("color: #7f8c8d; font-size: 12px; padding: 5px;")
        list_layout.addWidget(select_hint)
        
        list_group.setLayout(list_layout)
        top_layout.addWidget(list_group)
        
        # 通道操作
        action_group = QGroupBox("通道操作")
        action_layout = QHBoxLayout()
        
        # 添加通道按钮
        add_btn = QPushButton("➕ 添加通道")
        add_btn.clicked.connect(self.add_channel)
        action_layout.addWidget(add_btn)
        
        # 配置通道按钮
        config_btn = QPushButton("⚙️ 配置通道")
        config_btn.clicked.connect(self.config_channel)
        action_layout.addWidget(config_btn)
        
        # 测试通道按钮
        test_btn = QPushButton("🧪 测试通道")
        test_btn.clicked.connect(self.test_channel)
        action_layout.addWidget(test_btn)
        
        action_layout.addStretch()
        
        # 复制/导出按钮（下拉菜单）
        self.copy_export_btn = QPushButton("📋 复制/导出")
        self.copy_export_btn.clicked.connect(self.show_copy_export_menu)
        action_layout.addWidget(self.copy_export_btn)
        
        action_group.setLayout(action_layout)
        top_layout.addWidget(action_group)
        
        # 状态信息
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.StyledPanel)
        status_layout = QHBoxLayout(status_frame)
        
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("padding: 5px; background-color: #ecf0f1; border-radius: 3px;")
        
        self.selection_label = QLabel("已选择: 0 个通道")
        self.selection_label.setStyleSheet("padding: 5px; background-color: #ecf0f1; border-radius: 3px;")
        
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.selection_label)
        
        top_layout.addWidget(status_frame)
        
        # 下半部分：调试日志
        bottom_panel = QWidget()
        bottom_layout = QVBoxLayout(bottom_panel)
        
        # 调试日志标题和操作
        debug_header = QHBoxLayout()
        
        debug_title = QLabel("调试日志")
        debug_title_font = QFont()
        debug_title_font.setBold(True)
        debug_title.setFont(debug_title_font)
        debug_header.addWidget(debug_title)
        
        debug_header.addStretch()
        
        # 复制日志按钮
        copy_log_btn = QPushButton("📋 复制")
        copy_log_btn.clicked.connect(self.copy_debug_log)
        debug_header.addWidget(copy_log_btn)
        
        # 清空日志按钮
        clear_log_btn = QPushButton("🗑️ 清空")
        clear_log_btn.clicked.connect(self.clear_debug_log)
        debug_header.addWidget(clear_log_btn)
        
        bottom_layout.addLayout(debug_header)
        
        # 调试日志文本框
        self.debug_log_text = QTextEdit()
        self.debug_log_text.setReadOnly(True)
        self.debug_log_text.setFont(QFont("Consolas", 9))
        self.debug_log_text.setMaximumHeight(200)
        bottom_layout.addWidget(self.debug_log_text)
        
        # 日志级别选择
        log_level_layout = QHBoxLayout()
        log_level_layout.addWidget(QLabel("日志级别:"))
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self.log_level_combo.setCurrentText("INFO")
        log_level_layout.addWidget(self.log_level_combo)
        
        log_level_layout.addStretch()
        bottom_layout.addLayout(log_level_layout)
        
        # 添加到分割器
        splitter.addWidget(top_panel)
        splitter.addWidget(bottom_panel)
        splitter.setSizes([500, 200])
        
        layout.addWidget(splitter)
        
        # 初始化数据
        self.load_channels()
        
        # 添加初始调试日志
        self.add_debug_log("通道管理模块初始化完成", "INFO")
        self.add_debug_log(f"加载了 {len(self.channels)} 个通道", "INFO")
        self.add_debug_log("等待用户操作...", "INFO")
        
    def load_channels(self, channels=None):
        """加载通道到表格"""
        if channels is None:
            channels = self.filter_non_actual_channels(self.channels)
            
        self.channel_table.setRowCount(len(channels))
        self.selected_channels.clear()
        
        for i, channel in enumerate(channels):
            # 选择复选框
            checkbox_item = QTableWidgetItem()
            checkbox_item.setCheckState(Qt.Unchecked)
            checkbox_item.setData(Qt.UserRole, channel["id"])
            self.channel_table.setItem(i, 0, checkbox_item)
            
            # ID
            id_item = QTableWidgetItem(channel["id"])
            id_item.setData(Qt.UserRole, channel["id"])
            self.channel_table.setItem(i, 1, id_item)
            
            # App ID
            self.channel_table.setItem(i, 2, QTableWidgetItem(channel["app_id"]))
            
            # 账户ID
            self.channel_table.setItem(i, 3, QTableWidgetItem(channel["account_id"]))
            
            # 名称
            name_item = QTableWidgetItem(channel["name"])
            name_item.setToolTip(channel["name"])
            self.channel_table.setItem(i, 4, name_item)
            
            # 平台
            platform_item = QTableWidgetItem(channel["platform"])
            if channel["platform"] == "QQ":
                platform_item.setForeground(Qt.blue)
            elif channel["platform"] == "飞书":
                platform_item.setForeground(Qt.green)
            elif channel["platform"] == "微信":
                platform_item.setForeground(Qt.darkGreen)
            self.channel_table.setItem(i, 5, platform_item)
            
            # 平台名称
            platform_name_item = QTableWidgetItem(channel["platform_name"])
            platform_name_item.setToolTip(channel["platform_name"])
            self.channel_table.setItem(i, 6, platform_name_item)
            
            # 角色
            self.channel_table.setItem(i, 7, QTableWidgetItem(channel["role"]))
            
            # 状态
            status_item = QTableWidgetItem(channel["status"])
            if channel["status"] == "运行中":
                status_item.setForeground(Qt.darkGreen)
                status_item.setText("🟢 " + channel["status"])
            elif channel["status"] == "配置中":
                status_item.setForeground(Qt.darkYellow)
                status_item.setText("🟡 " + channel["status"])
            else:
                status_item.setForeground(Qt.darkRed)
                status_item.setText("🔴 " + channel["status"])
            self.channel_table.setItem(i, 8, status_item)
            
        self.update_selection_count()
        
    def on_item_clicked(self, item):
        """表格项点击事件"""
        if item.column() == 0:  # 复选框列
            channel_id = item.data(Qt.UserRole)
            if item.checkState() == Qt.Checked:
                self.selected_channels.add(channel_id)
                self.add_debug_log(f"选中通道: {channel_id}", "DEBUG")
            else:
                self.selected_channels.discard(channel_id)
                self.add_debug_log(f"取消选中通道: {channel_id}", "DEBUG")
            self.update_selection_count()
            
    def update_selection_count(self):
        """更新选择计数"""
        count = len(self.selected_channels)
        self.selection_label.setText(f"已选择: {count} 个通道")
        
    def on_search_changed(self):
        """搜索输入变化"""
        # 实时搜索（防抖）
        if hasattr(self, '_search_timer'):
            self._search_timer.stop()
            
        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self.search_channels_action)
        self._search_timer.start(500)  # 500ms防抖
        
    def search_channels_action(self):
        """搜索通道"""
        search_type_map = {
            "App ID": "app_id",
            "账户ID": "account_id",
            "平台名称": "platform_name",
            "角色": "role",
            "状态": "status",
            "全部字段": "all"
        }
        
        search_type = self.search_type_combo.currentText()
        search_key = search_type_map.get(search_type, "all")
        keyword = self.search_input.text().strip()
        
        channels = self.search_channels(search_key, keyword)
        self.load_channels(channels)
        
        if keyword:
            self.status_label.setText(f"搜索完成，找到 {len(channels)} 个通道")
            self.add_debug_log(f"搜索 '{keyword}' ({search_type})，找到 {len(channels)} 个通道", "INFO")
        else:
            self.status_label.setText("显示所有通道")
            
    def clear_search(self):
        """清空搜索"""
        self.search_input.clear()
        self.load_channels()
        self.status_label.setText("已清空搜索")
        self.add_debug_log("清空搜索条件", "INFO")
        
    def show_copy_export_menu(self):
        """显示复制/导出菜单"""
        menu = QMenu(self)
        
        # 第一级菜单：操作类型
        copy_menu = QMenu("📋 复制", self)
        export_menu = QMenu("📤 导出", self)
        
        # 复制子菜单
        copy_all_action = QAction("复制全部", self)
        copy_all_action.triggered.connect(lambda: self.copy_channels("all"))
        copy_menu.addAction(copy_all_action)
        
        copy_id_action = QAction("复制ID", self)
        copy_id_action.triggered.connect(lambda: self.copy_channels("id"))
        copy_menu.addAction(copy_id_action)
        
        copy_selected_action = QAction("复制选中", self)
        copy_selected_action.triggered.connect(lambda: self.copy_channels("selected"))
        copy_menu.addAction(copy_selected_action)
        
        # 导出子菜单
        export_all_action = QAction("导出全部", self)
        export_all_action.triggered.connect(lambda: self.export_channels("all"))
        export_menu.addAction(export_all_action)
        
        export_id_action = QAction("导出ID", self)
        export_id_action.triggered.connect(lambda: self.export_channels("id"))
        export_menu.addAction(export_id_action)
        
        export_selected_action = QAction("导出选中", self)
        export_selected_action.triggered.connect(lambda: self.export_channels("selected"))
        export_menu.addAction(export_selected_action)
        
        # 添加菜单项
        menu.addMenu(copy_menu)
        menu.addMenu(export_menu)
        
        # 显示菜单
        menu.exec_(self.copy_export_btn.mapToGlobal(self.copy_export_btn.rect().bottomLeft()))
        
    def copy_channels(self, copy_type):
        """复制通道信息"""
        import pyperclip
        
        try:
            text = ""
            
            if copy_type == "all":
                channels = self.filter_non_actual_channels(self.channels)
                text = self.format_channels_text(channels, "all")
                
            elif copy_type == "id":
                channels = self.filter_non_actual_channels(self.channels)
                text = self.format_channels_text(channels, "id")
                
            elif copy_type == "selected":
                selected_ids = list(self.selected_channels)
                channels = [c for c in self.channels if c["id"] in selected_ids]
                if not channels:
                    QMessageBox.warning(self, "复制失败", "请先选择要复制的通道")
                    self.add_debug_log("复制失败：未选择通道", "WARNING")
                    return
                text = self.format_channels_text(channels, "all")
                
            if text:
                pyperclip.copy(text)
                self.status_label.setText("已复制到剪贴板")
                self.add_debug_log(f"复制 {len(channels)} 个通道信息到剪贴板", "INFO")
                QMessageBox.information(self, "复制成功", "通道信息已复制到剪贴板")
            else:
                QMessageBox.warning(self, "复制失败", "没有可复制的通道信息")
                self.add_debug_log("复制失败：没有可复制的通道信息", "WARNING")
                
        except ImportError:
            QMessageBox.warning(self, "复制失败", "需要安装pyperclip库: pip install pyperclip")
            self.add_debug_log("复制失败：缺少pyperclip库", "ERROR")
        except Exception as e:
            self.status_label.setText(f"复制失败: {str(e)}")
            self.add_debug_log(f"复制失败: {str(e)}", "ERROR")
            QMessageBox.warning(self, "复制失败", f"复制过程中出错:\n{str(e)}")
            
    def export_channels(self, export_type):
        """导出通道信息"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if export_type == "all":
                channels = self.filter_non_actual_channels(self.channels)
                filename = f"channels_all_{timestamp}.txt"
                content = self.format_channels_text(channels, "all")
                
            elif export_type == "id":
                channels = self.filter_non_actual_channels(self.channels)
                filename = f"channels_id_{timestamp}.txt"
                content = self.format_channels_text(channels, "id")
                
            elif export_type == "selected":
                selected_ids = list(self.selected_channels)
                channels = [c for c in self.channels if c["id"] in selected_ids]
                if not channels:
                    QMessageBox.warning(self, "导出失败", "请先选择要导出的通道")
                    self.add_debug_log("导出失败：未选择通道", "WARNING")
                    return
                filename = f"channels_selected_{timestamp}.txt"
                content = self.format_channels_text(channels, "all")
                
            if content:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                self.status_label.setText(f"已导出到: {filename}")
                self.add_debug_log(f"导出 {len(channels)} 个通道信息到 {filename}", "INFO")
                QMessageBox.information(self, "导出成功", 
                                      f"通道信息已成功导出到:\n{filename}\n\n"
                                      f"导出类型: {export_type}\n"
                                      f"通道数量: {len(channels)}")
            else:
                QMessageBox.warning(self, "导出失败", "没有可导出的通道信息")
                self.add_debug_log("导出失败：没有可导出的通道信息", "WARNING")
                
        except Exception as e:
            self.status_label.setText(f"导出失败: {str(e)}")
            self.add_debug_log(f"导出失败: {str(e)}", "ERROR")
            QMessageBox.warning(self, "导出失败", f"导出过程中出错:\n{str(e)}")
            
    def format_channels_text(self, channels, format_type):
        """格式化通道文本"""
        if format_type == "id":
            # 只导出ID
            return "\n".join([channel["id"] for channel in channels])
        else:
            # 导出完整信息
            lines = []
            lines.append("码泓mahong OpenClaw管理器 - 通道列表")
            lines.append(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append(f"通道数量: {len(channels)}")
            lines.append("="*50)
            
            for i, channel in enumerate(channels, 1):
                lines.append(f"\n通道 #{i}:")
                lines.append(f"  ID: {channel['id']}")
                lines.append(f"  App ID: {channel['app_id']}")
                lines.append(f"  账户ID: {channel['account_id']}")
                lines.append(f"  名称: {channel['name']}")
                lines.append(f"  平台: {channel['platform']}")
                lines.append(f"  平台名称: {channel['platform_name']}")
                lines.append(f"  角色: {channel['role']}")
                lines.append(f"  状态: {channel['status']}")
                lines.append(f"  配置状态: {channel['config_status']}")
                lines.append(f"  创建时间: {channel['created_at']}")
                
            return "\n".join(lines)
            
    def copy_debug_log(self):
        """复制调试日志"""
        import pyperclip
        
        try:
            log_text = self.debug_log_text.toPlainText()
            if log_text:
                pyperclip.copy(log_text)
                self.add_debug_log("调试日志已复制到剪贴板", "INFO")
                QMessageBox.information(self, "复制成功", "调试日志已复制到剪贴板")
            else:
                QMessageBox.warning(self, "复制失败", "调试日志为空")
                self.add_debug_log("复制失败：调试日志为空", "WARNING")
        except ImportError:
            QMessageBox.warning(self, "复制失败", "需要安装pyperclip库: pip install pyperclip")
            self.add_debug_log("复制失败：缺少pyperclip库", "ERROR")
        except Exception as e:
            self.add_debug_log(f"复制调试日志失败: {str(e)}", "ERROR")
            QMessageBox.warning(self, "复制失败", f"复制调试日志时出错:\n{str(e)}")
            
    def clear_debug_log(self):
        """清空调试日志"""
        self.debug_logs.clear()
        self.debug_log_text.clear()
        self.add_debug_log("调试日志已清空", "INFO")
        
    def add_channel(self):
        """添加通道"""
        self.status_label.setText("添加通道功能开发中...")
        self.add_debug_log("用户点击添加通道按钮", "INFO")
        QMessageBox.information(self, "添加通道", "添加通道功能正在开发中")
        
    def config_channel(self):
        """配置通道"""
        if not self.selected_channels:
            QMessageBox.warning(self, "配置通道", "请先选择要配置的通道")
            self.add_debug_log("配置通道失败：未选择通道", "WARNING")
            return
            
        self.status_label.setText(f"正在配置 {len(self.selected_channels)} 个通道...")
        self.add_debug_log(f"开始配置 {len(self.selected_channels)} 个选中的通道", "INFO")
        QMessageBox.information(self, "配置通道", 
                              f"正在配置选中的 {len(self.selected_channels)} 个通道\n\n"
                              f"配置功能正在开发中")
        
    def test_channel(self):
        """测试通道"""
        if not self.selected_channels:
            QMessageBox.warning(self, "测试通道", "请先选择要测试的通道")
            self.add_debug_log("测试通道失败：未选择通道", "WARNING")
            return
            
        self.status_label.setText(f"正在测试 {len(self.selected_channels)} 个通道...")
        self.add_debug_log(f"开始测试 {len(self.selected_channels)} 个选中的通道", "INFO")
        QMessageBox.information(self, "测试通道", 
                              f"正在测试选中的 {len(self.selected_channels)} 个通道\n\n"
                              f"测试功能正在开发中")

# 测试函数
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = ChannelManagerIntegrated()
    window.setWindowTitle("集成版通道管理测试")
    window.resize(1000, 800)
    window.show()
    sys.exit(app.exec())