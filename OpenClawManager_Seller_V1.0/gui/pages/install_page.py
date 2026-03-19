#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装/卸载页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QProgressBar, QFileDialog, QGroupBox
)
from PySide6.QtCore import Qt


class InstallPage(QWidget):
    """安装/卸载页面"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 安装区域
        install_group = QGroupBox("安装OpenClaw")
        install_layout = QVBoxLayout(install_group)
        install_layout.setSpacing(15)
        
        # 安装路径
        path_layout = QHBoxLayout()
        path_label = QLabel("安装路径:")
        self.path_edit = QLineEdit()
        self.path_edit.setText("C:\\OpenClaw")
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self.browse_path)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(browse_btn)
        install_layout.addLayout(path_layout)
        
        # 镜像源
        mirror_layout = QHBoxLayout()
        mirror_label = QLabel("镜像源:")
        self.mirror_combo = QComboBox()
        self.mirror_combo.addItems(["自动", "淘宝", "华为", "腾讯", "官方"])
        mirror_layout.addWidget(mirror_label)
        mirror_layout.addWidget(self.mirror_combo)
        install_layout.addLayout(mirror_layout)
        
        # 安装按钮和进度条
        btn_layout = QHBoxLayout()
        self.install_btn = QPushButton("开始安装")
        self.install_btn.clicked.connect(self.start_install)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        btn_layout.addWidget(self.install_btn)
        btn_layout.addWidget(self.progress_bar)
        install_layout.addLayout(btn_layout)
        
        # 卸载区域
        uninstall_group = QGroupBox("卸载OpenClaw")
        uninstall_layout = QVBoxLayout(uninstall_group)
        uninstall_layout.setSpacing(15)
        
        # 卸载路径
        uninstall_path_layout = QHBoxLayout()
        uninstall_path_label = QLabel("卸载路径:")
        self.uninstall_path_edit = QLineEdit()
        self.uninstall_path_edit.setText("C:\\OpenClaw")
        uninstall_browse_btn = QPushButton("浏览")
        uninstall_browse_btn.clicked.connect(self.browse_uninstall_path)
        uninstall_path_layout.addWidget(uninstall_path_label)
        uninstall_path_layout.addWidget(self.uninstall_path_edit)
        uninstall_path_layout.addWidget(uninstall_browse_btn)
        uninstall_layout.addLayout(uninstall_path_layout)
        
        # 卸载按钮
        self.uninstall_btn = QPushButton("开始卸载")
        self.uninstall_btn.clicked.connect(self.start_uninstall)
        uninstall_layout.addWidget(self.uninstall_btn)
        
        layout.addWidget(install_group)
        layout.addWidget(uninstall_group)
        layout.addStretch()
    
    def browse_path(self):
        """浏览安装路径"""
        path = QFileDialog.getExistingDirectory(self, "选择安装目录")
        if path:
            self.path_edit.setText(path)
    
    def browse_uninstall_path(self):
        """浏览卸载路径"""
        path = QFileDialog.getExistingDirectory(self, "选择卸载目录")
        if path:
            self.uninstall_path_edit.setText(path)
    
    def start_install(self):
        """开始安装"""
        # 这里将集成现有的安装器模块
        self.progress_bar.setValue(50)
        # 模拟安装过程
        from PySide6.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self.progress_bar.setValue(100))
    
    def start_uninstall(self):
        """开始卸载"""
        # 这里将集成现有的卸载器模块
        pass