#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
帮助页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QTabWidget
)
from PySide6.QtCore import Qt


class HelpPage(QWidget):
    """帮助页面"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 使用说明标签
        usage_tab = QTextEdit()
        usage_tab.setReadOnly(True)
        usage_tab.setHtml("""
        <h2>使用说明</h2>
        <h3>1. 授权管理</h3>
        <p>- 查阅网店站内通知获取激活码</p>
        <p>- 如需协助，请联系网店客服</p>
        <p>- 输入激活码并点击激活按钮</p>
        
        <h3>2. 安装OpenClaw</h3>
        <p>- 选择安装路径（默认：C:\OpenClaw）</p>
        <p>- 选择镜像源（推荐：自动）</p>
        <p>- 点击开始安装按钮</p>
        
        <h3>3. 模型管理</h3>
        <p>- 点击添加模型按钮</p>
        <p>- 填写模型名称、提供商、API Key和Base URL，详情请查阅模型厂商的技术文档</p>
        <p>- 点击测试连接按钮验证模型是否可用</p>
        
        <h3>4. 通道管理</h3>
        <p>- 点击启动通道配置工具按钮</p>
        <p>- 根据向导配置通道参数</p>
        <p>- 点击查看当前配置按钮查看已配置的通道</p>
        
        <h3>5. Agent管理</h3>
        <p>- 输入Agent名称并选择类型</p>
        <p>- 点击创建按钮创建Agent</p>
        <p>- 选中Agent后点击管理按钮进行管理</p>
        """)
        tab_widget.addTab(usage_tab, "使用说明")
        
        # 常见问题标签
        faq_tab = QTextEdit()
        faq_tab.setReadOnly(True)
        faq_tab.setHtml("""
        <h2>常见问题</h2>
        <h3>Q: 安装失败怎么办？</h3>
        <p>A: 请检查网络连接，尝试更换镜像源，或以管理员身份运行程序</p>
        
        <h3>Q: 激活码无效怎么办？</h3>
        <p>A: 请确认激活码是否正确，或联系客服获取新的激活码</p>
        
        <h3>Q: 模型测试失败怎么办？</h3>
        <p>A: 请检查API Key是否正确，网络连接是否正常，或联系模型提供商</p>
        
        <h3>Q: 程序无法启动怎么办？</h3>
        <p>A: 请检查是否安装了必要的运行环境，或重新下载程序</p>
        """)
        tab_widget.addTab(faq_tab, "常见问题")
        
        # 技术支持标签
        support_tab = QTextEdit()
        support_tab.setReadOnly(True)
        support_tab.setHtml("""
        <h2>技术支持</h2>
        <p><strong>官方网站：</strong>https://openclaw.io</p>
        <p><strong>客服邮箱：</strong>support@openclaw.io</p>
        <p><strong>技术论坛：</strong>https://forum.openclaw.io</p>
        <p><strong>GitHub：</strong>https://github.com/openclaw</p>
        <p><strong>版本：</strong>v1.0</p>
        <p><strong>更新日期：</strong>2026年3月16日</p>
        
        <h3>5. Agent管理</h3>
        <p>请登录IM平台的开放平台申请，详情请查阅官方操作手册：</p>
        <ul>
        <li><strong>飞书：</strong>https://open.feishu.cn</li>
        <li><strong>QQ：</strong>https://q.qq.com/#/</li>
        <li><strong>微信：</strong>https://open.weixin.qq.com/</li>
        <li><strong>企业微信：</strong>https://developer.work.weixin.qq.com/</li>
        <li><strong>钉钉：</strong>https://open.dingtalk.com/</li>
        </ul>
        <p>其他平台，请根据官方的链接为准。</p>
        """)
        tab_widget.addTab(support_tab, "技术支持")
        
        layout.addWidget(tab_widget)
