#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
买家版设置页面 - 包含授权管理
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox,
    QGroupBox, QHBoxLayout, QMessageBox, QComboBox, QTextEdit
)
from PySide6.QtCore import Qt
import uuid
import hashlib
from datetime import datetime


class BuyerSettingsPage(QWidget):
    """买家版设置页面（包含授权管理）"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        # 授权管理区域
        auth_group = QGroupBox("授权管理 (License Management)")
        auth_layout = QVBoxLayout(auth_group)
        
        # 机器码显示
        machine_code_layout = QHBoxLayout()
        machine_label = QLabel("机器码 (Machine Code):")
        machine_code_layout.addWidget(machine_label)
        
        self.machine_code_label = QLabel(self.get_machine_code())
        self.machine_code_label.setStyleSheet("font-family: monospace; background-color: #f5f5f5; padding: 5px; border: 1px solid #ddd;")
        machine_code_layout.addWidget(self.machine_code_label)
        
        # 复制按钮
        copy_button = QPushButton("复制 (Copy)")
        copy_button.clicked.connect(self.copy_machine_code)
        machine_code_layout.addWidget(copy_button)
        
        auth_layout.addLayout(machine_code_layout)
        
        # 激活码输入
        activate_layout = QHBoxLayout()
        activate_label = QLabel("激活码 (Activation Code):")
        activate_layout.addWidget(activate_label)
        
        self.activate_input = QLineEdit()
        self.activate_input.setPlaceholderText("请输入16位激活码")
        self.activate_input.setMaxLength(16)
        activate_layout.addWidget(self.activate_input)
        
        auth_layout.addLayout(activate_layout)
        
        # 激活按钮
        activate_button_layout = QHBoxLayout()
        self.activate_button = QPushButton("激活 (Activate)")
        self.activate_button.clicked.connect(self.activate_license)
        activate_button_layout.addWidget(self.activate_button)
        
        self.check_status_button = QPushButton("检查状态 (Check Status)")
        self.check_status_button.clicked.connect(self.check_license_status)
        activate_button_layout.addWidget(self.check_status_button)
        
        auth_layout.addLayout(activate_button_layout)
        
        # 授权状态显示
        self.status_label = QLabel("状态: 未激活 (Status: Not Activated)")
        self.status_label.setStyleSheet("font-weight: bold; color: #dc3545;")
        auth_layout.addWidget(self.status_label)
        
        layout.addWidget(auth_group)
        
        # 通用设置区域
        general_group = QGroupBox("通用设置 (General Settings)")
        general_layout = QVBoxLayout(general_group)
        
        # 开机自启动
        self.auto_start_check = QCheckBox("开机自启动 (Auto Start)")
        self.auto_start_check.setToolTip("Automatically start with Windows")
        general_layout.addWidget(self.auto_start_check)
        
        # 最小化到托盘
        self.minimize_to_tray_check = QCheckBox("最小化到托盘 (Minimize to Tray)")
        self.minimize_to_tray_check.setToolTip("Minimize to system tray instead of taskbar")
        general_layout.addWidget(self.minimize_to_tray_check)
        
        # 自动检查更新
        self.auto_update_check = QCheckBox("自动检查更新 (Auto Check Updates)")
        self.auto_update_check.setToolTip("Automatically check for updates")
        general_layout.addWidget(self.auto_update_check)
        
        # 语言设置
        lang_layout = QHBoxLayout()
        lang_label = QLabel("界面语言 (Interface Language):")
        lang_layout.addWidget(lang_label)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("中文 (Chinese)", "zh")
        self.lang_combo.addItem("English", "en")
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        
        general_layout.addLayout(lang_layout)
        
        # 保存按钮
        save_btn = QPushButton("保存设置 (Save Settings)")
        save_btn.setToolTip("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        
        layout.addWidget(general_group)
        layout.addWidget(save_btn)
        
        # Gateway管理区域
        gateway_group = QGroupBox("Gateway管理 (Gateway Management)")
        gateway_layout = QVBoxLayout(gateway_group)
        
        # Gateway状态显示
        gateway_status_layout = QHBoxLayout()
        gateway_status_label = QLabel("Gateway状态 (Gateway Status):")
        gateway_status_layout.addWidget(gateway_status_label)
        
        self.gateway_status_label = QLabel("未知 (Unknown)")
        self.gateway_status_label.setStyleSheet("font-weight: bold; color: #666;")
        gateway_status_layout.addWidget(self.gateway_status_label)
        
        gateway_status_layout.addStretch()
        gateway_layout.addLayout(gateway_status_layout)
        
        # Gateway操作按钮
        gateway_buttons_layout = QHBoxLayout()
        
        self.check_gateway_btn = QPushButton("检查状态 (Check Status)")
        self.check_gateway_btn.clicked.connect(self.check_gateway_status)
        gateway_buttons_layout.addWidget(self.check_gateway_btn)
        
        self.restart_gateway_btn = QPushButton("重启网关 (Restart Gateway)")
        self.restart_gateway_btn.clicked.connect(self.restart_gateway)
        gateway_buttons_layout.addWidget(self.restart_gateway_btn)
        
        self.open_monitor_btn = QPushButton("打开监控 (Open Monitor)")
        self.open_monitor_btn.clicked.connect(self.open_gateway_monitor)
        gateway_buttons_layout.addWidget(self.open_monitor_btn)
        
        gateway_buttons_layout.addStretch()
        gateway_layout.addLayout(gateway_buttons_layout)
        
        layout.addWidget(gateway_group)
        
        # 加载当前设置
        self.load_settings()
        
        # 初始化Gateway状态检查
        self.check_gateway_status()
    
    def get_machine_code(self):
        """获取机器码"""
        # 生成基于系统信息的机器码
        try:
            # 使用主机名和MAC地址生成机器码
            import socket
            import uuid as uuid_module
            
            hostname = socket.gethostname()
            mac = ':'.join(['{:02x}'.format((uuid_module.getnode() >> elements) & 0xff) 
                           for elements in range(0, 2*6, 2)][::-1])
            
            # 生成哈希值作为机器码
            machine_info = f"{hostname}_{mac}"
            machine_hash = hashlib.md5(machine_info.encode()).hexdigest()[:16].upper()
            
            # 格式化为XXXX-XXXX-XXXX-XXXX
            formatted_code = '-'.join([machine_hash[i:i+4] for i in range(0, 16, 4)])
            return formatted_code
        except:
            # 如果获取失败，使用随机UUID
            random_uuid = str(uuid.uuid4()).replace('-', '').upper()[:16]
            return '-'.join([random_uuid[i:i+4] for i in range(0, 16, 4)])
    
    def copy_machine_code(self):
        """复制机器码到剪贴板"""
        from PySide6.QtGui import QGuiApplication
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.machine_code_label.text())
        QMessageBox.information(self, "复制成功", "机器码已复制到剪贴板")
    
    def activate_license(self):
        """激活授权"""
        activation_code = self.activate_input.text().strip()
        
        if not activation_code:
            QMessageBox.warning(self, "输入错误", "请输入激活码")
            return
        
        if len(activation_code) != 16:
            QMessageBox.warning(self, "输入错误", "激活码应为16位字符")
            return
        
        # 根据激活码判断版本类型
        # 实际应该调用服务器验证，这里模拟逻辑
        license_type = self.detect_license_type(activation_code)
        
        # 保存授权信息
        self.license_info = {
            "code": activation_code,
            "type": license_type,
            "activated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "machine_code": self.machine_code_label.text()
        }
        
        # 更新界面
        status_text = f"状态: 已激活 ({license_type})"
        self.status_label.setText(status_text)
        self.status_label.setStyleSheet("font-weight: bold; color: #28a745;")
        
        # 更新主窗口的授权状态
        main_window = self.window()
        if hasattr(main_window, 'update_license_status'):
            main_window.update_license_status("已授权")
            # 传递授权类型信息
            if hasattr(main_window, 'set_license_type'):
                main_window.set_license_type(license_type)
        
        # 更新通道管理页面的授权类型
        if hasattr(main_window, 'pages') and 'channel' in main_window.pages:
            channel_page = main_window.pages['channel']
            if hasattr(channel_page, 'set_license_type'):
                channel_page.set_license_type(license_type)
        
        QMessageBox.information(
            self,
            "激活成功",
            f"软件激活成功！\n\n"
            f"机器码: {self.machine_code_label.text()}\n"
            f"激活码: {activation_code}\n"
            f"授权类型: {license_type}\n"
            f"激活时间: {self.license_info['activated_at']}\n\n"
            f"授权状态已更新为: 已授权"
        )
    
    def detect_license_type(self, activation_code):
        """检测授权码类型（模拟逻辑）"""
        # 实际应该调用服务器验证
        # 这里根据激活码格式模拟判断
        
        # 简单模拟：根据激活码前缀判断
        if activation_code.startswith("BASIC"):
            return "基础版"
        elif activation_code.startswith("PRO"):
            return "专业版"
        else:
            # 默认根据价格判断：79元为基础版，149元为专业版
            # 这里随机分配用于演示
            import random
            return "基础版" if random.random() < 0.5 else "专业版"
    
    def check_license_status(self):
        """检查授权状态"""
        # 这里应该检查实际的授权状态
        # 暂时显示模拟状态
        if self.status_label.text().startswith("状态: 已激活"):
            QMessageBox.information(self, "授权状态", "软件已激活，授权状态正常")
        else:
            QMessageBox.warning(self, "授权状态", "软件未激活，请先激活授权")
    
    def load_settings(self):
        """加载设置"""
        # 这里应该从配置文件加载设置
        # 暂时使用默认值
        self.auto_start_check.setChecked(True)
        self.minimize_to_tray_check.setChecked(True)
        self.auto_update_check.setChecked(True)
        self.lang_combo.setCurrentIndex(0)  # 默认中文
    
    def save_settings(self):
        """保存设置"""
        # 获取设置值
        auto_start = self.auto_start_check.isChecked()
        minimize_to_tray = self.minimize_to_tray_check.isChecked()
        auto_update = self.auto_update_check.isChecked()
        language = self.lang_combo.currentData()
        
        # 这里应该保存到配置文件
        # 暂时只显示保存成功的消息
        
        QMessageBox.information(
            self,
            "保存成功",
            "设置已保存 (Settings saved successfully)."
        )
    
    def check_gateway_status(self):
        """检查Gateway状态"""
        try:
            # 模拟检查Gateway状态
            # 实际应该调用openclaw gateway status命令
            import subprocess
            import sys
            
            # 尝试执行openclaw gateway status命令
            result = subprocess.run(
                ["openclaw", "gateway", "status"],
                capture_output=True,
                text=True,
                shell=True
            )
            
            if result.returncode == 0:
                if "running" in result.stdout.lower():
                    self.gateway_status_label.setText("运行中 (Running)")
                    self.gateway_status_label.setStyleSheet("font-weight: bold; color: #28a745;")
                else:
                    self.gateway_status_label.setText("已停止 (Stopped)")
                    self.gateway_status_label.setStyleSheet("font-weight: bold; color: #dc3545;")
            else:
                self.gateway_status_label.setText("未知 (Unknown)")
                self.gateway_status_label.setStyleSheet("font-weight: bold; color: #666;")
                
        except Exception as e:
            # 如果命令执行失败，显示未知状态
            self.gateway_status_label.setText("未知 (Unknown)")
            self.gateway_status_label.setStyleSheet("font-weight: bold; color: #666;")
    
    def restart_gateway(self):
        """重启Gateway"""
        reply = QMessageBox.question(
            self,
            "确认重启",
            "确定要重启Gateway吗？这可能会中断正在进行的连接。\n\n"
            "Are you sure you want to restart the Gateway? This may interrupt ongoing connections.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # 显示重启中状态
                self.gateway_status_label.setText("重启中 (Restarting...)")
                self.gateway_status_label.setStyleSheet("font-weight: bold; color: #ffc107;")
                
                # 模拟重启Gateway
                # 实际应该调用openclaw gateway restart命令
                import subprocess
                import time
                
                # 停止Gateway
                subprocess.run(["openclaw", "gateway", "stop"], capture_output=True, shell=True)
                time.sleep(2)  # 等待2秒
                
                # 启动Gateway
                subprocess.run(["openclaw", "gateway", "start"], capture_output=True, shell=True)
                time.sleep(3)  # 等待3秒
                
                # 检查状态
                self.check_gateway_status()
                
                QMessageBox.information(
                    self,
                    "重启完成",
                    "Gateway已成功重启。\n\n"
                    "Gateway has been restarted successfully."
                )
                
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "重启失败",
                    f"Gateway重启失败: {str(e)}\n\n"
                    f"Gateway restart failed: {str(e)}"
                )
                self.check_gateway_status()
    
    def open_gateway_monitor(self):
        """打开Gateway监控窗口"""
        try:
            from gui.pages.gateway_monitor_page import GatewayMonitorPage
            
            # 创建并显示监控窗口
            self.monitor_window = GatewayMonitorPage()
            self.monitor_window.show()
            
        except ImportError as e:
            QMessageBox.warning(
                self,
                "功能未完成",
                "Gateway监控窗口功能正在开发中...\n\n"
                f"错误: {str(e)}"
            )