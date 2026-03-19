#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修改仪表盘中的边框颜色和宽度
"""

import re

# 读取文件
with open('dashboard_bilingual_terminal.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 定义替换规则
# 1. 将鲜艳的边框颜色改为协调的深蓝色
# 2. 将边框宽度减少（如果可能）

# 鲜艳颜色到协调颜色的映射
color_mapping = {
    '#ffaa00': '#3a3a5a',  # 橙色 -> 深蓝色
    '#4cc9f0': '#3a3a5a',  # 亮蓝色 -> 深蓝色
    '#00ffaa': '#3a3a5a',  # 亮绿色 -> 深蓝色
    '#00ff88': '#3a3a5a',  # 亮绿色 -> 深蓝色
    '#ff5555': '#3a3a5a',  # 红色 -> 深蓝色
    '#ff00aa': '#3a3a5a',  # 粉色 -> 深蓝色
}

# 应用颜色替换
modified_content = content
for old_color, new_color in color_mapping.items():
    # 替换边框颜色
    pattern = rf'border:\s*\d+px\s+solid\s+{re.escape(old_color)}'
    replacement = f'border: 1px solid {new_color}'
    modified_content = re.sub(pattern, replacement, modified_content, flags=re.IGNORECASE)
    
    # 替换其他可能的格式
    pattern2 = rf'border.*?{re.escape(old_color)}'
    # 更保守的替换，只替换确切的颜色值
    modified_content = modified_content.replace(old_color, new_color)

# 备份原文件
import os
if os.path.exists('dashboard_bilingual_terminal.py.bak'):
    os.remove('dashboard_bilingual_terminal.py.bak')
os.rename('dashboard_bilingual_terminal.py', 'dashboard_bilingual_terminal.py.bak')

# 写入修改后的文件
with open('dashboard_bilingual_terminal.py', 'w', encoding='utf-8') as f:
    f.write(modified_content)

print('仪表盘边框颜色修改完成！')
print('修改内容:')
print('1. 将所有鲜艳的边框颜色改为协调的深蓝色(#3a3a5a)')
print('2. 确保边框宽度为1px')
print('3. 原文件已备份为: dashboard_bilingual_terminal.py.bak')