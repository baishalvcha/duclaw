#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卖家版帮助页面
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QTabWidget
)
from PySide6.QtCore import Qt


class SellerHelpPage(QWidget):
    """卖家版帮助页面"""
    
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
        <h2>卖家版使用说明</h2>
        
        <h3>1. 授权码批量生成</h3>
        <p><strong>步骤：</strong></p>
        <ol>
        <li>打开"授权管理"页面</li>
        <li>设置生成数量（1-9990）</li>
        <li>点击"生成授权码"按钮</li>
        <li>生成完成后，授权码会显示在列表中</li>
        <li>点击"导出授权码"按钮保存到文件</li>
        </ol>
        
        <h3>2. 授权码格式</h3>
        <p>生成的授权码格式为：<code>XXXX-XXXX-XXXX-XXXX</code></p>
        <ul>
        <li>共16位字符（大写字母和数字）</li>
        <li>每4位用连字符分隔</li>
        <li>示例：<code>AB12-CD34-EF56-GH78</code></li>
        </ul>
        
        <h3>3. 授权码管理</h3>
        <p><strong>导出功能：</strong></p>
        <ul>
        <li>支持导出为TXT文本文件</li>
        <li>文件包含生成时间、数量等信息</li>
        <li>建议按批次导出和管理</li>
        </ul>
        
        <p><strong>清空功能：</strong></p>
        <ul>
        <li>可以清空当前生成的授权码列表</li>
        <li>清空前会提示确认</li>
        <li>建议导出后再清空</li>
        </ul>
        
        <h3>4. 设置功能</h3>
        <p>卖家版提供基本的设置功能：</p>
        <ul>
        <li><strong>开机自启动：</strong>设置软件是否随系统启动</li>
        <li><strong>最小化到托盘：</strong>关闭窗口时最小化到系统托盘</li>
        <li><strong>自动检查更新：</strong>自动检查软件更新</li>
        <li><strong>界面语言：</strong>切换中英文界面</li>
        </ul>
        """)
        tab_widget.addTab(usage_tab, "使用说明")
        
        # 技术支持标签
        support_tab = QTextEdit()
        support_tab.setReadOnly(True)
        support_tab.setHtml("""
        <h2>技术支持</h2>
        
        <h3>官方信息</h3>
        <p><strong>软件名称：</strong>码泓mahong-openclaw管理器-卖家版</p>
        <p><strong>版本：</strong>V1.0</p>
        <p><strong>更新日期：</strong>2026年3月18日</p>
        <p><strong>版权所有：</strong>© 2026 码泓 mahong</p>
        <p><strong>官方网站：</strong>https://mahong.openclaw.ai</p>
        
        <h3>联系方式</h3>
        <p><strong>客服支持：</strong>通过淘宝店铺联系客服</p>
        <p><strong>技术支持：</strong>QQ技术支持群（购买后获取）</p>
        <p><strong>问题反馈：</strong>使用中遇到的问题请及时反馈</p>
        
        <h3>注意事项</h3>
        <p><strong>授权码管理：</strong></p>
        <ul>
        <li>妥善保管生成的授权码文件</li>
        <li>建议按销售批次管理授权码</li>
        <li>避免授权码泄露或重复使用</li>
        </ul>
        
        <p><strong>软件使用：</strong></p>
        <ul>
        <li>本软件为卖家专用工具</li>
        <li>仅限合法用途使用</li>
        <li>禁止用于非法或侵权用途</li>
        </ul>
        
        <h3>更新计划</h3>
        <p><strong>V1.0 版本功能：</strong></p>
        <ul>
        <li>授权码批量生成</li>
        <li>授权码导出功能</li>
        <li>基础设置功能</li>
        </ul>
        
        <p><strong>后续版本计划：</strong></p>
        <ul>
        <li>授权码激活状态管理</li>
        <li>销售统计功能</li>
        <li>更多导出格式支持</li>
        </ul>
        """)
        tab_widget.addTab(support_tab, "技术支持")
        
        # 关于标签
        about_tab = QTextEdit()
        about_tab.setReadOnly(True)
        about_tab.setHtml("""
        <h2>关于卖家版</h2>
        
        <h3>软件简介</h3>
        <p><strong>码泓mahong-openclaw管理器-卖家版</strong>是一款专为卖家设计的授权码批量管理工具。</p>
        <p>主要功能包括：</p>
        <ul>
        <li>批量生成授权码（1-9990个）</li>
        <li>授权码导出和管理</li>
        <li>简洁易用的操作界面</li>
        <li>基础设置功能</li>
        </ul>
        
        <h3>开发背景</h3>
        <p>本软件是为配合"码泓mahong-openclaw管理器"产品销售而开发的配套工具。</p>
        <p>旨在帮助卖家：</p>
        <ul>
        <li>高效管理软件授权码</li>
        <li>简化销售流程</li>
        <li>提升客户服务质量</li>
        </ul>
        
        <h3>技术特点</h3>
        <p><strong>安全性：</strong></p>
        <ul>
        <li>本地运行，数据安全</li>
        <li>不收集用户信息</li>
        <li>授权码本地生成</li>
        </ul>
        
        <p><strong>易用性：</strong></p>
        <ul>
        <li>图形化操作界面</li>
        <li>简洁明了的操作流程</li>
        <li>实时反馈和提示</li>
        </ul>
        
        <p><strong>稳定性：</strong></p>
        <ul>
        <li>经过严格测试</li>
        <li>稳定的授权码生成算法</li>
        <li>可靠的文件导出功能</li>
        </ul>
        
        <h3>版权声明</h3>
        <p><strong>版权所有：</strong>© 2026 码泓 mahong</p>
        <p><strong>许可协议：</strong>本软件受版权法保护，未经许可不得复制、修改或分发。</p>
        <p><strong>使用限制：</strong>仅限购买"码泓mahong-openclaw管理器"的卖家使用。</p>
        
        <h3>免责声明</h3>
        <p>1. 本软件按"现状"提供，不提供任何明示或暗示的担保。</p>
        <p>2. 使用者应自行承担使用风险。</p>
        <p>3. 开发者不对因使用本软件造成的任何损失负责。</p>
        <p>4. 禁止将本软件用于非法用途。</p>
        </ul>
        """)
        tab_widget.addTab(about_tab, "关于")
        
        layout.addWidget(tab_widget)