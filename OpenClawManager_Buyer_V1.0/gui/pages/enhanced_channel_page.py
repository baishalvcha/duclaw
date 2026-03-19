#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版通道管理页面 - 包含版本限制功能
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QGroupBox, QTextEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QProgressBar
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QBrush


class EnhancedChannelPage(QWidget):
    """增强版通道管理页面（包含版本限制）"""
    
    def __init__(self):
        super().__init__()
        self.agent_counts = {}  # 各平台Agent数量统计
        self.license_type = "未激活"  # 默认未激活
        self.init_ui()
        self.load_agent_data()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 版本信息区域
        version_group = QGroupBox("版本信息")
        version_layout = QVBoxLayout(version_group)
        
        self.version_label = QLabel("当前版本: 未激活")
        self.version_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        version_layout.addWidget(self.version_label)
        
        # 版本限制说明
        limits_text = QLabel("版本限制说明：")
        limits_text.setStyleSheet("font-weight: bold; margin-top: 10px;")
        version_layout.addWidget(limits_text)
        
        limits_info = QTextEdit()
        limits_info.setReadOnly(True)
        limits_info.setMaximumHeight(120)
        limits_info.setPlainText(
            "🔸 基础版（79元）：\n"
            "   • 每个IM平台最多创建5个Agent\n"
            "   • 支持所有基础功能\n"
            "   • 永久授权，免费更新\n\n"
            "🔸 专业版（149元）：\n"
            "   • 无Agent数量限制\n"
            "   • 支持所有高级功能\n"
            "   • 永久授权，优先技术支持\n"
        )
        version_layout.addWidget(limits_info)
        
        layout.addWidget(version_group)
        
        # Agent管理区域
        agent_group = QGroupBox("Agent管理")
        agent_layout = QVBoxLayout(agent_group)
        
        # 平台选择
        platform_layout = QHBoxLayout()
        platform_label = QLabel("选择平台:")
        platform_layout.addWidget(platform_label)
        
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(["飞书", "QQ", "微信", "企业微信", "钉钉", "Discord", "Slack"])
        platform_layout.addWidget(self.platform_combo)
        
        # 添加Agent按钮
        self.add_agent_btn = QPushButton("添加Agent")
        self.add_agent_btn.clicked.connect(self.add_agent)
        platform_layout.addWidget(self.add_agent_btn)
        
        platform_layout.addStretch()
        agent_layout.addLayout(platform_layout)
        
        # Agent统计表格
        self.agent_table = QTableWidget()
        self.agent_table.setColumnCount(4)
        self.agent_table.setHorizontalHeaderLabels(["平台", "Agent数量", "限制数量", "状态"])
        self.agent_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.agent_table.setEditTriggers(QTableWidget.NoEditTriggers)
        agent_layout.addWidget(self.agent_table)
        
        # 统计信息
        stats_layout = QHBoxLayout()
        self.total_label = QLabel("总计: 0个Agent")
        self.limit_label = QLabel("限制: -")
        self.status_label = QLabel("状态: 正常")
        
        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.limit_label)
        stats_layout.addWidget(self.status_label)
        stats_layout.addStretch()
        
        agent_layout.addLayout(stats_layout)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        refresh_btn = QPushButton("刷新")
        refresh_btn.clicked.connect(self.refresh_data)
        clear_btn = QPushButton("清空测试数据")
        clear_btn.clicked.connect(self.clear_test_data)
        
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        
        agent_layout.addLayout(button_layout)
        
        layout.addWidget(agent_group)
        
        # 平台申请指引
        guide_group = QGroupBox("平台申请指引")
        guide_layout = QVBoxLayout(guide_group)
        
        guide_text = QTextEdit()
        guide_text.setReadOnly(True)
        guide_text.setPlainText(
            "📋 Agent申请指引：\n\n"
            "1. 飞书：https://open.feishu.cn\n"
            "   • 注册开发者账号\n"
            "   • 创建企业自建应用\n"
            "   • 获取App ID和App Secret\n\n"
            "2. QQ：https://q.qq.com/#/\n"
            "   • 注册QQ开放平台\n"
            "   • 创建机器人应用\n"
            "   • 获取App ID和Token\n\n"
            "3. 微信：https://open.weixin.qq.com/\n"
            "   • 注册微信开放平台\n"
            "   • 创建公众号或小程序\n"
            "   • 获取App ID和Secret\n\n"
            "4. 其他平台请参考官方文档"
        )
        guide_layout.addWidget(guide_text)
        
        layout.addWidget(guide_group)
        
        # 定时刷新数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(5000)  # 5秒刷新一次
    
    def set_license_type(self, license_type):
        """设置授权类型"""
        self.license_type = license_type
        self.version_label.setText(f"当前版本: {license_type}")
        self.update_ui_limits()
    
    def get_platform_limit(self, platform):
        """获取平台限制数量"""
        if self.license_type == "基础版":
            return 5  # 基础版每个平台限制5个
        elif self.license_type == "专业版":
            return 999  # 专业版无限制（设置一个较大值）
        else:
            return 0  # 未激活
    
    def add_agent(self):
        """添加Agent"""
        platform = self.platform_combo.currentText()
        
        # 检查授权状态
        if self.license_type == "未激活":
            QMessageBox.warning(self, "未激活", "请先激活软件授权才能添加Agent")
            return
        
        # 检查平台限制
        current_count = self.agent_counts.get(platform, 0)
        platform_limit = self.get_platform_limit(platform)
        
        if platform_limit > 0 and current_count >= platform_limit:
            QMessageBox.warning(
                self,
                "达到限制",
                f"{platform}平台已达到限制数量（{platform_limit}个）\n\n"
                f"当前版本: {self.license_type}\n"
                f"如需添加更多Agent，请升级到专业版"
            )
            return
        
        # 模拟添加Agent
        self.agent_counts[platform] = current_count + 1
        
        # 显示成功消息
        QMessageBox.information(
            self,
            "添加成功",
            f"已成功添加{platform}平台的Agent\n\n"
            f"当前{platform}平台Agent数量: {self.agent_counts[platform]}/{platform_limit}"
        )
        
        # 刷新界面
        self.refresh_data()
    
    def load_agent_data(self):
        """加载Agent数据（模拟）"""
        # 模拟一些测试数据
        platforms = ["飞书", "QQ", "微信", "企业微信", "钉钉"]
        for platform in platforms:
            self.agent_counts[platform] = 2  # 每个平台默认2个Agent
    
    def refresh_data(self):
        """刷新数据"""
        # 更新表格
        self.agent_table.setRowCount(len(self.agent_counts))
        
        total_agents = 0
        row = 0
        
        for platform, count in self.agent_counts.items():
            limit = self.get_platform_limit(platform)
            total_agents += count
            
            # 平台名称
            platform_item = QTableWidgetItem(platform)
            self.agent_table.setItem(row, 0, platform_item)
            
            # Agent数量
            count_item = QTableWidgetItem(str(count))
            self.agent_table.setItem(row, 1, count_item)
            
            # 限制数量
            limit_text = str(limit) if limit > 0 else "无限制"
            limit_item = QTableWidgetItem(limit_text)
            self.agent_table.setItem(row, 2, limit_item)
            
            # 状态
            status = "正常"
            color = QColor(40, 167, 69)  # 绿色
            
            if limit > 0 and count >= limit:
                status = "已达上限"
                color = QColor(220, 53, 69)  # 红色
            elif limit > 0 and count >= limit * 0.8:  # 达到80%警告
                status = "接近上限"
                color = QColor(255, 193, 7)  # 黄色
            
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QBrush(color))
            self.agent_table.setItem(row, 3, status_item)
            
            row += 1
        
        # 更新统计信息
        self.total_label.setText(f"总计: {total_agents}个Agent")
        
        if self.license_type == "基础版":
            self.limit_label.setText("限制: 每个平台最多5个Agent")
        elif self.license_type == "专业版":
            self.limit_label.setText("限制: 无限制")
        else:
            self.limit_label.setText("限制: 请先激活授权")
        
        # 更新状态
        if total_agents == 0:
            self.status_label.setText("状态: 暂无Agent")
            self.status_label.setStyleSheet("color: #666;")
        else:
            self.status_label.setText("状态: 运行中")
            self.status_label.setStyleSheet("color: #28a745;")
    
    def clear_test_data(self):
        """清空测试数据"""
        reply = QMessageBox.question(
            self,
            "确认清空",
            "确定要清空所有测试Agent数据吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.agent_counts = {}
            self.refresh_data()
            QMessageBox.information(self, "已清空", "测试数据已清空")
    
    def update_ui_limits(self):
        """根据授权类型更新UI限制"""
        # 更新按钮状态
        if self.license_type == "未激活":
            self.add_agent_btn.setEnabled(False)
            self.add_agent_btn.setText("请先激活授权")
        else:
            self.add_agent_btn.setEnabled(True)
            self.add_agent_btn.setText("添加Agent")
        
        # 刷新数据
        self.refresh_data()


# 导入QComboBox
from PySide6.QtWidgets import QComboBox