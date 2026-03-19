#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度云上传页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QTextEdit, QFileDialog, QMessageBox, QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal
import os

from gui.language import language_manager


class UploadThread(QThread):
    """上传线程"""
    progress = Signal(int)
    finished = Signal(bool, str)
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        """模拟上传过程"""
        try:
            # 模拟上传进度
            for i in range(101):
                self.progress.emit(i)
                self.msleep(50)  # 模拟上传时间
            # 模拟上传成功
            file_name = os.path.basename(self.file_path)
            download_link = f"https://pan.baidu.com/s/1234567890abcdef?filename={file_name}"
            self.finished.emit(True, download_link)
        except Exception as e:
            self.finished.emit(False, str(e))


class BaiduPage(QWidget):
    """百度云上传页面"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.upload_thread = None
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel(language_manager.get("nav_baidu"))
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # 描述
        desc_label = QLabel("上传文件到百度云并获取分享链接")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # 文件选择
        file_layout = QHBoxLayout()
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("选择要上传的文件")
        self.file_path_edit.setReadOnly(True)
        file_layout.addWidget(self.file_path_edit)
        
        browse_button = QPushButton("浏览")
        browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(browse_button)
        
        layout.addLayout(file_layout)
        
        # 上传按钮
        upload_button = QPushButton("上传到百度云")
        upload_button.clicked.connect(self.upload_file)
        layout.addWidget(upload_button)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 结果显示
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(100)
        layout.addWidget(self.result_text)
        
        self.setLayout(layout)
    
    def browse_file(self):
        """浏览选择文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "", "所有文件 (*.*)"
        )
        if file_path:
            self.file_path_edit.setText(file_path)
    
    def upload_file(self):
        """上传文件"""
        file_path = self.file_path_edit.text().strip()
        
        if not file_path:
            QMessageBox.warning(self, "警告", "请选择要上传的文件")
            return
        
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "警告", "文件不存在")
            return
        
        # 开始上传
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 创建并启动上传线程
        self.upload_thread = UploadThread(file_path)
        self.upload_thread.progress.connect(self.update_progress)
        self.upload_thread.finished.connect(self.upload_finished)
        self.upload_thread.start()
    
    def update_progress(self, value):
        """更新上传进度"""
        self.progress_bar.setValue(value)
    
    def upload_finished(self, success, message):
        """上传完成处理"""
        self.progress_bar.setVisible(False)
        
        if success:
            self.result_text.setText(f"上传成功！\n分享链接: {message}")
            QMessageBox.information(self, "成功", "文件上传成功")
        else:
            self.result_text.setText(f"上传失败: {message}")
            QMessageBox.warning(self, "错误", f"上传失败: {message}")