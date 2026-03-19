#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
码泓mahong-OpenClaw管理器 v1.0（GUI版）
主程序入口
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QLocale, QTranslator

from gui.main_window import MainWindow


def main():
    """主函数"""
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("码泓mahong-OpenClaw管理器")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("OpenClaw Team")
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()