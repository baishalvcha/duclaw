#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卖家版授权管理页面 - 批量生成授权码
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit,
    QHBoxLayout, QGroupBox, QMessageBox, QSpinBox, QComboBox, QDateEdit
)
from PySide6.QtCore import Qt, QDate
import random
import string
from datetime import datetime


class SellerAuthPage(QWidget):
    """卖家版授权管理页面"""
    
    def __init__(self):
        super().__init__()
        self.generated_codes = []  # 存储生成的授权码
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        # 标题
        title_label = QLabel("🔑 授权管理 - 批量生成授权码")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)
        
        # 批量生成授权码区域
        batch_group = QGroupBox("批量生成授权码")
        batch_layout = QVBoxLayout(batch_group)
        
        # 数量设置
        count_layout = QHBoxLayout()
        count_label = QLabel("生成数量 (1-9999):")
        count_layout.addWidget(count_label)
        
        self.count_spinbox = QSpinBox()
        self.count_spinbox.setMinimum(1)
        self.count_spinbox.setMaximum(9999)
        self.count_spinbox.setValue(10)
        self.count_spinbox.setSuffix(" 个")
        count_layout.addWidget(self.count_spinbox)
        
        batch_layout.addLayout(count_layout)
        
        # 有效期设置
        validity_layout = QHBoxLayout()
        validity_label = QLabel("授权有效期:")
        validity_layout.addWidget(validity_label)
        
        self.validity_combo = QComboBox()
        self.validity_combo.addItem("永久", "permanent")
        self.validity_combo.addItem("试用", "trial")
        self.validity_combo.currentIndexChanged.connect(self.on_validity_changed)
        validity_layout.addWidget(self.validity_combo)
        
        # 有效期日期控件（默认隐藏）
        self.date_layout = QHBoxLayout()
        self.date_layout.setContentsMargins(20, 0, 0, 0)
        
        start_label = QLabel("开始日期:")
        self.date_layout.addWidget(start_label)
        
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())
        self.start_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_layout.addWidget(self.start_date_edit)
        
        end_label = QLabel("结束日期:")
        self.date_layout.addWidget(end_label)
        
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate().addDays(30))  # 默认30天试用
        self.end_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_layout.addWidget(self.end_date_edit)
        
        self.date_layout.addStretch()
        
        # 初始隐藏日期控件
        self.date_widget = QWidget()
        self.date_widget.setLayout(self.date_layout)
        self.date_widget.hide()
        
        batch_layout.addLayout(validity_layout)
        batch_layout.addWidget(self.date_widget)
        
        # 生成按钮
        generate_button = QPushButton("生成授权码")
        generate_button.clicked.connect(self.generate_batch_codes)
        batch_layout.addWidget(generate_button)
        
        # 生成结果
        self.batch_result_text = QTextEdit()
        self.batch_result_text.setReadOnly(True)
        self.batch_result_text.setFixedHeight(300)
        self.batch_result_text.setPlaceholderText("生成的授权码将显示在这里")
        batch_layout.addWidget(self.batch_result_text)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        # 导出按钮
        export_button = QPushButton("导出授权码")
        export_button.clicked.connect(self.export_codes)
        button_layout.addWidget(export_button)
        
        # 清空按钮
        clear_button = QPushButton("清空列表")
        clear_button.clicked.connect(self.clear_codes)
        button_layout.addWidget(clear_button)
        
        batch_layout.addLayout(button_layout)
        
        layout.addWidget(batch_group)
        
        # 统计信息
        self.stats_label = QLabel("已生成: 0 个授权码")
        self.stats_label.setStyleSheet("font-size: 12px; color: #666; margin-top: 10px;")
        layout.addWidget(self.stats_label)
        
        layout.addStretch()
    
    def on_validity_changed(self, index):
        """有效期类型切换"""
        validity_type = self.validity_combo.itemData(index)
        if validity_type == "trial":
            self.date_widget.show()
        else:
            self.date_widget.hide()
    
    def generate_license_code(self, validity_type="permanent", start_date=None, end_date=None):
        """生成单个授权码（包含有效期信息）"""
        # 生成16位授权码，格式：XXXX-XXXX-XXXX-XXXX
        characters = string.ascii_uppercase + string.digits
        code = ''.join(random.choice(characters) for _ in range(16))
        
        # 格式化为XXXX-XXXX-XXXX-XXXX
        formatted_code = '-'.join([code[i:i+4] for i in range(0, 16, 4)])
        
        # 添加有效期信息
        validity_info = {
            "code": formatted_code,
            "validity_type": validity_type,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if validity_type == "trial" and start_date and end_date:
            validity_info["start_date"] = start_date.toString("yyyy-MM-dd")
            validity_info["end_date"] = end_date.toString("yyyy-MM-dd")
        
        return validity_info
    
    def generate_batch_codes(self):
        """批量生成授权码"""
        count = self.count_spinbox.value()
        
        if count <= 0:
            QMessageBox.warning(self, "输入错误", "生成数量必须大于0")
            return
        
        if count > 9999:
            QMessageBox.warning(self, "输入错误", "生成数量不能超过9999")
            return
        
        # 清空之前的生成结果
        self.generated_codes = []
        self.batch_result_text.clear()
        
        # 获取有效期设置
        validity_type = self.validity_combo.currentData()
        start_date = self.start_date_edit.date() if validity_type == "trial" else None
        end_date = self.end_date_edit.date() if validity_type == "trial" else None
        
        # 生成授权码
        validity_text = "永久授权" if validity_type == "permanent" else f"试用授权 ({start_date.toString('yyyy-MM-dd')} 至 {end_date.toString('yyyy-MM-dd')})"
        codes_text = f"批量生成的授权码 - {validity_text}\n"
        codes_text += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        codes_text += "=" * 60 + "\n\n"
        
        for i in range(count):
            code_info = self.generate_license_code(validity_type, start_date, end_date)
            self.generated_codes.append(code_info)
            
            if validity_type == "permanent":
                codes_text += f"{i+1:4d}. {code_info['code']} (永久)\n"
            else:
                codes_text += f"{i+1:4d}. {code_info['code']} (试用: {code_info['start_date']} - {code_info['end_date']})\n"
            
            # 每生成100个更新一次显示
            if (i + 1) % 100 == 0:
                self.batch_result_text.setText(codes_text + f"\n正在生成... ({i+1}/{count})")
                QApplication.processEvents()  # 更新界面
        
        codes_text += "\n" + "=" * 50 + "\n"
        codes_text += f"总计: {count} 个授权码\n"
        codes_text += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        self.batch_result_text.setText(codes_text)
        self.update_stats()
        
        QMessageBox.information(
            self,
            "生成成功",
            f"已成功生成 {count} 个授权码"
        )
    
    def export_codes(self):
        """导出授权码到文件"""
        if not self.generated_codes:
            QMessageBox.warning(self, "警告", "没有可导出的授权码")
            return
        
        from PySide6.QtWidgets import QFileDialog
        import os
        
        # 生成默认文件名
        default_name = f"授权码_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存授权码文件", default_name, "文本文件 (*.txt)"
        )
        
        if file_path:
            try:
                # 准备导出内容
                export_content = f"码泓mahong-openclaw管理器 授权码列表\n"
                export_content += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                export_content += f"数量: {len(self.generated_codes)} 个\n"
                
                # 添加有效期信息
                if self.generated_codes and 'validity_type' in self.generated_codes[0]:
                    validity_type = self.generated_codes[0]['validity_type']
                    if validity_type == "permanent":
                        export_content += "授权类型: 永久授权\n"
                    else:
                        export_content += f"授权类型: 试用授权\n"
                        export_content += f"开始日期: {self.generated_codes[0]['start_date']}\n"
                        export_content += f"结束日期: {self.generated_codes[0]['end_date']}\n"
                
                export_content += "=" * 60 + "\n\n"
                
                for i, code_info in enumerate(self.generated_codes, 1):
                    if isinstance(code_info, dict) and 'code' in code_info:
                        code = code_info['code']
                        if code_info['validity_type'] == "permanent":
                            export_content += f"{i:4d}. {code} (永久)\n"
                        else:
                            export_content += f"{i:4d}. {code} (试用: {code_info['start_date']} - {code_info['end_date']})\n"
                    else:
                        # 兼容旧格式
                        export_content += f"{i:4d}. {code_info}\n"
                
                export_content += "\n" + "=" * 50 + "\n"
                export_content += "© 2026 码泓 mahong 版权所有\n"
                export_content += "官方网站: https://mahong.openclaw.ai"
                
                # 写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(export_content)
                
                QMessageBox.information(
                    self,
                    "导出成功",
                    f"授权码已导出到文件:\n{file_path}\n\n共导出 {len(self.generated_codes)} 个授权码"
                )
                
            except Exception as e:
                QMessageBox.warning(self, "导出失败", f"导出过程中发生错误:\n{str(e)}")
    
    def clear_codes(self):
        """清空授权码列表"""
        if not self.generated_codes:
            return
        
        reply = QMessageBox.question(
            self,
            "确认清空",
            f"确定要清空 {len(self.generated_codes)} 个授权码吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.generated_codes = []
            self.batch_result_text.clear()
            self.update_stats()
            QMessageBox.information(self, "已清空", "授权码列表已清空")
    
    def update_stats(self):
        """更新统计信息"""
        count = len(self.generated_codes)
        self.stats_label.setText(f"已生成: {count} 个授权码")


# 导入QApplication用于界面更新
from PySide6.QtWidgets import QApplication