#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QCheckBox, QComboBox, QGroupBox, QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal

from gui.language import language_manager
from integration.cli_integration import CLIIntegration


class SettingsPage(QWidget):
    """设置页面"""
    
    def __init__(self):
        super().__init__()
        self.cli_integration = CLIIntegration()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 通用设置
        general_group = QGroupBox(language_manager.get("settings_general"))
        general_layout = QVBoxLayout(general_group)
        
        self.startup_check = QCheckBox(language_manager.get("settings_startup"))
        self.startup_check.setToolTip("Run on Startup")
        self.tray_check = QCheckBox(language_manager.get("settings_tray"))
        self.tray_check.setToolTip("Minimize to Tray")
        general_layout.addWidget(self.startup_check)
        general_layout.addWidget(self.tray_check)
        
        # 保存按钮
        save_btn = QPushButton(language_manager.get("settings_save"))
        save_btn.setToolTip("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        
        layout.addWidget(general_group)
        layout.addWidget(save_btn)
        layout.addStretch()
    
    def check_update(self):
        """检查更新"""
        # 这里将集成现有的更新检查功能
        print("检查更新")
    
    def save_settings(self):
        """保存设置"""
        settings = {
            "startup": self.startup_check.isChecked(),
            "tray": self.tray_check.isChecked()
        }
        
        # 这里将保存设置到配置文件
        print(f"保存设置: {settings}")
        
        # 提示用户设置已保存
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "提示 (Information)",
            "设置已保存 (Settings saved successfully)."
        )
    
    def check_gateway_status(self):
        """检查网关状态"""
        # 模拟检查网关状态
        self.status_indicator.setText("检查中...")
        self.status_indicator.setStyleSheet("font-weight: bold; color: #337ab7;")
        
        # 异步执行命令
        def output_callback(output):
            print(f"输出: {output}")
        
        def error_callback(error):
            print(f"错误: {error}")
            self.status_indicator.setText("异常")
            self.status_indicator.setStyleSheet("font-weight: bold; color: #dc3545;")
        
        def done_callback(returncode):
            if returncode == 0:
                self.status_indicator.setText("运行中")
                self.status_indicator.setStyleSheet("font-weight: bold; color: #28a745;")
            else:
                self.status_indicator.setText("未运行")
                self.status_indicator.setStyleSheet("font-weight: bold; color: #dc3545;")
        
        # 执行网关状态检查命令
        self.cli_integration.execute_openclaw_command_async(
            "gateway status",
            output_callback,
            error_callback,
            done_callback
        )
    
    def restart_gateway(self):
        """重启网关"""
        # 显示确认对话框
        reply = QMessageBox.question(
            self,
            "确认重启",
            "确定要重启网关吗？这将暂时中断服务。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.restart_btn.setEnabled(False)
        
        # 模拟重启过程
        def output_callback(output):
            print(f"输出: {output}")
        
        def error_callback(error):
            print(f"错误: {error}")
            QMessageBox.warning(self, "错误", f"重启失败: {error}")
            self.progress_bar.setVisible(False)
            self.restart_btn.setEnabled(True)
        
        def done_callback(returncode):
            if returncode == 0:
                self.progress_bar.setValue(100)
                QMessageBox.information(self, "成功", "网关重启成功")
                # 检查重启后的状态
                self.check_gateway_status()
            else:
                QMessageBox.warning(self, "错误", "重启失败")
            self.progress_bar.setVisible(False)
            self.restart_btn.setEnabled(True)
        
        # 执行重启命令
        self.cli_integration.execute_openclaw_command_async(
            "gateway restart",
            output_callback,
            error_callback,
            done_callback
        )
        
        # 模拟进度更新
        def update_progress():
            for i in range(1, 101):
                if not self.cli_integration.is_command_running():
                    break
                self.progress_bar.setValue(i)
                import time
                time.sleep(0.1)
        
        import threading
        progress_thread = threading.Thread(target=update_progress)
        progress_thread.daemon = True
        progress_thread.start()