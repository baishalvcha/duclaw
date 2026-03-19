#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
码泓mahong-openclaw管理器-卖家版V1.0
卖家版主程序入口
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QLocale, QTranslator
from gui.seller_main_window import SellerMainWindow


def main():
    """主函数"""
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("码泓mahong-openclaw管理器-卖家版")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("码泓 mahong")
    
    # 创建主窗口
    window = SellerMainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()