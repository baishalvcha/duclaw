#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模型管理模块 - 腾讯云风格
支持模型Coding Plan和模型API配置
"""

import sys
import json
from datetime import datetime
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                              QTreeWidget, QTreeWidgetItem, QTableWidget,
                              QTableWidgetItem, QPushButton, QLabel, QLineEdit,
                              QTextEdit, QComboBox, QTabWidget, QSplitter,
                              QHeaderView, QMessageBox, QFormLayout, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class ModelManagerTencent(QWidget):
    """腾讯云风格模型管理器"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("模型管理 - 腾讯云风格")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; padding: 10px 0;")
        layout.addWidget(title_label)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧：模型树
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # 模型分类树
        model_tree_group = QGroupBox("模型分类")
        model_tree_layout = QVBoxLayout()
        
        self.model_tree = QTreeWidget()
        self.model_tree.setHeaderLabel("模型列表")
        self.model_tree.setColumnCount(1)
        
        # 构建模型树
        self.build_model_tree()
        
        model_tree_layout.addWidget(self.model_tree)
        model_tree_group.setLayout(model_tree_layout)
        left_layout.addWidget(model_tree_group)
        
        # 快速操作
        quick_group = QGroupBox("快速操作")
        quick_layout = QVBoxLayout()
        
        add_model_btn = QPushButton("➕ 添加模型")
        add_model_btn.clicked.connect(self.add_model)
        
        test_model_btn = QPushButton("🧪 测试连接")
        test_model_btn.clicked.connect(self.test_connection)
        
        import_model_btn = QPushButton("📥 导入配置")
        import_model_btn.clicked.connect(self.import_config)
        
        export_model_btn = QPushButton("📤 导出配置")
        export_model_btn.clicked.connect(self.export_config)
        
        quick_layout.addWidget(add_model_btn)
        quick_layout.addWidget(test_model_btn)
        quick_layout.addWidget(import_model_btn)
        quick_layout.addWidget(export_model_btn)
        quick_layout.addStretch()
        
        quick_group.setLayout(quick_layout)
        left_layout.addWidget(quick_group)
        
        # 右侧：配置面板
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # 创建标签页
        self.config_tabs = QTabWidget()
        
        # JSON输入标签页
        self.json_tab = self.create_json_tab()
        self.config_tabs.addTab(self.json_tab, "JSON输入")
        
        # 表单输入标签页
        self.form_tab = self.create_form_tab()
        self.config_tabs.addTab(self.form_tab, "表单输入")
        
        # 代码示例标签页
        self.code_tab = self.create_code_tab()
        self.config_tabs.addTab(self.code_tab, "代码示例")
        
        right_layout.addWidget(self.config_tabs)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 保存配置")
        save_btn.clicked.connect(self.save_config)
        
        reset_btn = QPushButton("🔄 重置")
        reset_btn.clicked.connect(self.reset_config)
        
        validate_btn = QPushButton("✅ 验证配置")
        validate_btn.clicked.connect(self.validate_config)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addWidget(validate_btn)
        button_layout.addStretch()
        
        right_layout.addLayout(button_layout)
        
        # 状态信息
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.StyledPanel)
        status_layout = QHBoxLayout(status_frame)
        
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("padding: 5px; background-color: #ecf0f1; border-radius: 3px;")
        
        self.model_count_label = QLabel("模型数量: 0")
        self.model_count_label.setStyleSheet("padding: 5px; background-color: #ecf0f1; border-radius: 3px;")
        
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.model_count_label)
        
        right_layout.addWidget(status_frame)
        
        # 添加到分割器
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        
        layout.addWidget(splitter)
        
        # 连接树选择事件
        self.model_tree.itemClicked.connect(self.on_model_selected)
        
        # 更新模型计数
        self.update_model_count()
        
    def build_model_tree(self):
        """构建模型树"""
        # 清空树
        self.model_tree.clear()
        
        # 模型Coding Plan
        coding_plan_item = QTreeWidgetItem(self.model_tree, ["模型 Coding Plan"])
        # coding_plan_item.setIcon(0, self.style().standardIcon(self.style().SP_DirIcon))
        
        coding_plan_items = [
            "腾讯云Coding Plan",
            "百炼 Coding Plan", 
            "MiniMax (国内-Coding Plan)",
            "智谱AI(GLM国内-Coding Plan)",
            "智谱AI(GLM国际-Coding Plan)",
            "方舟(火山引擎)Coding Plan"
        ]
        
        for item_text in coding_plan_items:
            item = QTreeWidgetItem(coding_plan_item, [item_text])
            # item.setIcon(0, self.style().standardIcon(self.style().SP_FileIcon))
            item.setData(0, Qt.UserRole, {"type": "coding_plan", "name": item_text})
            
        # 模型API
        model_api_item = QTreeWidgetItem(self.model_tree, ["模型API"])
        # model_api_item.setIcon(0, self.style().standardIcon(self.style().SP_DirIcon))
        
        model_api_items = [
            "腾讯混元",
            "腾讯云 DeepSeek",
            "深度求索(DeepSeek)",
            "百炼(千问)",
            "MiniMax(国内)",
            "MiniMax(国际)",
            "Moonshot AI(Kimi国内)",
            "Moonshot AI(Kimi国际)",
            "智谱AI(GLM国内)",
            "智谱AI(GLM国际)",
            "火山引擎(豆包)",
            "百度(文心一言)"
        ]
        
        for item_text in model_api_items:
            item = QTreeWidgetItem(model_api_item, [item_text])
            # item.setIcon(0, self.style().standardIcon(self.style().SP_FileIcon))
            item.setData(0, Qt.UserRole, {"type": "model_api", "name": item_text})
            
        # 展开所有项
        self.model_tree.expandAll()
        
    def create_json_tab(self):
        """创建JSON输入标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # JSON编辑器
        json_group = QGroupBox("JSON配置")
        json_layout = QVBoxLayout()
        
        self.json_editor = QTextEdit()
        self.json_editor.setPlaceholderText("""{
  "provider": "tencent",
  "base_url": "https://api.tencent.com/v1",
  "api_key": "your-api-key-here",
  "model": {
    "id": "deepseek-chat",
    "name": "DeepSeek Chat"
  },
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 2000
  }
}""")
        self.json_editor.setFont(QFont("Consolas", 10))
        json_layout.addWidget(self.json_editor)
        
        # JSON操作按钮
        json_btn_layout = QHBoxLayout()
        
        format_btn = QPushButton("🔄 格式化")
        format_btn.clicked.connect(self.format_json)
        
        validate_json_btn = QPushButton("✅ 验证JSON")
        validate_json_btn.clicked.connect(self.validate_json)
        
        load_example_btn = QPushButton("📋 加载示例")
        load_example_btn.clicked.connect(self.load_json_example)
        
        json_btn_layout.addWidget(format_btn)
        json_btn_layout.addWidget(validate_json_btn)
        json_btn_layout.addWidget(load_example_btn)
        json_btn_layout.addStretch()
        
        json_layout.addLayout(json_btn_layout)
        json_group.setLayout(json_layout)
        layout.addWidget(json_group)
        
        # JSON提示
        hint_label = QLabel("提示: 支持标准的JSON格式，配置完成后点击'验证JSON'检查格式")
        hint_label.setStyleSheet("color: #7f8c8d; font-size: 12px; padding: 5px;")
        layout.addWidget(hint_label)
        
        layout.addStretch()
        
        return tab
        
    def create_form_tab(self):
        """创建表单输入标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 表单配置
        form_group = QGroupBox("表单配置")
        form_layout = QFormLayout()
        
        # Provider
        self.provider_input = QLineEdit()
        self.provider_input.setPlaceholderText("请输入自定义模型 provider")
        form_layout.addRow("Provider:", self.provider_input)
        
        # Base URL
        self.base_url_input = QLineEdit()
        self.base_url_input.setPlaceholderText("请输入自定义模型 base_url")
        form_layout.addRow("Base URL:", self.base_url_input)
        
        # API
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("请输入自定义模型 api")
        form_layout.addRow("API:", self.api_input)
        
        # API Key
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("请输入自定义模型 api_key")
        self.api_key_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("API Key:", self.api_key_input)
        
        # Model ID
        self.model_id_input = QLineEdit()
        self.model_id_input.setPlaceholderText("请输入自定义模型 model.id")
        form_layout.addRow("Model ID:", self.model_id_input)
        
        # Model Name
        self.model_name_input = QLineEdit()
        self.model_name_input.setPlaceholderText("请输入自定义模型 model.name")
        form_layout.addRow("Model Name:", self.model_name_input)
        
        # 模型类型选择
        self.model_type_combo = QComboBox()
        self.model_type_combo.addItems([
            "聊天模型",
            "文本生成",
            "代码生成", 
            "图像生成",
            "语音识别",
            "自定义"
        ])
        form_layout.addRow("模型类型:", self.model_type_combo)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # 表单操作按钮
        form_btn_layout = QHBoxLayout()
        
        fill_example_btn = QPushButton("📋 填充示例")
        fill_example_btn.clicked.connect(self.fill_form_example)
        
        clear_form_btn = QPushButton("🗑️ 清空表单")
        clear_form_btn.clicked.connect(self.clear_form)
        
        generate_json_btn = QPushButton("🔄 生成JSON")
        generate_json_btn.clicked.connect(self.generate_json_from_form)
        
        form_btn_layout.addWidget(fill_example_btn)
        form_btn_layout.addWidget(clear_form_btn)
        form_btn_layout.addWidget(generate_json_btn)
        form_btn_layout.addStretch()
        
        layout.addLayout(form_btn_layout)
        
        layout.addStretch()
        
        return tab
        
    def create_code_tab(self):
        """创建代码示例标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 代码示例选择
        code_group = QGroupBox("代码示例")
        code_layout = QVBoxLayout()
        
        # 示例选择
        example_layout = QHBoxLayout()
        example_layout.addWidget(QLabel("选择示例:"))
        
        self.example_combo = QComboBox()
        self.example_combo.addItems([
            "Python - 基本调用",
            "Python - 流式响应",
            "Python - 批量处理",
            "JavaScript - 基本调用",
            "cURL - 命令行调用"
        ])
        self.example_combo.currentIndexChanged.connect(self.update_code_example)
        example_layout.addWidget(self.example_combo)
        example_layout.addStretch()
        
        code_layout.addLayout(example_layout)
        
        # 代码编辑器
        self.code_editor = QTextEdit()
        self.code_editor.setReadOnly(True)
        self.code_editor.setFont(QFont("Consolas", 10))
        code_layout.addWidget(self.code_editor)
        
        # 代码操作按钮
        code_btn_layout = QHBoxLayout()
        
        copy_code_btn = QPushButton("📋 复制代码")
        copy_code_btn.clicked.connect(self.copy_code)
        
        run_code_btn = QPushButton("▶️ 运行测试")
        run_code_btn.clicked.connect(self.run_code_test)
        
        code_btn_layout.addWidget(copy_code_btn)
        code_btn_layout.addWidget(run_code_btn)
        code_btn_layout.addStretch()
        
        code_layout.addLayout(code_btn_layout)
        code_group.setLayout(code_layout)
        layout.addWidget(code_group)
        
        # 初始化代码示例
        self.update_code_example()
        
        layout.addStretch()
        
        return tab
        
    def on_model_selected(self, item, column):
        """模型选择事件"""
        data = item.data(0, Qt.UserRole)
        if data:
            model_type = data.get("type")
            model_name = data.get("name")
            
            if model_type == "coding_plan":
                self.status_label.setText(f"选择: {model_name} (Coding Plan)")
                self.load_coding_plan_example(model_name)
            elif model_type == "model_api":
                self.status_label.setText(f"选择: {model_name} (模型API)")
                self.load_model_api_example(model_name)
                
    def load_coding_plan_example(self, plan_name):
        """加载Coding Plan示例"""
        examples = {
            "腾讯云Coding Plan": """{
  "plan_name": "腾讯云Coding Plan",
  "provider": "tencent",
  "features": ["代码补全", "代码审查", "单元测试生成"],
  "quota": {
    "monthly_tokens": 1000000,
    "concurrent_requests": 10
  }
}""",
            "百炼 Coding Plan": """{
  "plan_name": "百炼 Coding Plan",
  "provider": "bailian",
  "features": ["代码生成", "代码优化", "安全检测"],
  "quota": {
    "monthly_tokens": 500000,
    "concurrent_requests": 5
  }
}""",
            "MiniMax (国内-Coding Plan)": """{
  "plan_name": "MiniMax Coding Plan",
  "provider": "minimax",
  "features": ["智能编程", "代码解释", "文档生成"],
  "quota": {
    "monthly_tokens": 300000,
    "concurrent_requests": 3
  }
}"""
        }
        
        example = examples.get(plan_name, """{
  "plan_name": "自定义Coding Plan",
  "provider": "custom",
  "features": [],
  "quota": {
    "monthly_tokens": 100000,
    "concurrent_requests": 1
  }
}""")
        
        self.json_editor.setText(example)
        
    def load_model_api_example(self, api_name):
        """加载模型API示例"""
        examples = {
            "腾讯混元": """{
  "provider": "tencent_hunyuan",
  "base_url": "https://hunyuan.tencent.com/api/v1",
  "api_key": "your-tencent-api-key",
  "model": {
    "id": "hunyuan-pro",
    "name": "腾讯混元 Pro"
  }
}""",
            "腾讯云 DeepSeek": """{
  "provider": "tencent_deepseek",
  "base_url": "https://api.tencent.com/deepseek/v1",
  "api_key": "your-tencent-deepseek-key",
  "model": {
    "id": "deepseek-chat",
    "name": "DeepSeek Chat"
  }
}""",
            "深度求索(DeepSeek)": """{
  "provider": "deepseek",
  "base_url": "https://api.deepseek.com/v1",
  "api_key": "your-deepseek-api-key",
  "model": {
    "id": "deepseek-chat",
    "name": "DeepSeek Chat"
  }
}""",
            "百炼(千问)": """{
  "provider": "bailian",
  "base_url": "https://api.bailian.aliyun.com/v1",
  "api_key": "your-bailian-api-key",
  "model": {
    "id": "qwen-max",
    "name": "通义千问 Max"
  }
}""",
            "MiniMax(国内)": """{
  "provider": "minimax_cn",
  "base_url": "https://api.minimax.cn/v1",
  "api_key": "your-minimax-cn-key",
  "model": {
    "id": "abab5.5-chat",
    "name": "MiniMax ABAB 5.5"
  }
}"""
        }
        
        example = examples.get(api_name, """{
  "provider": "custom",
  "base_url": "https://api.example.com/v1",
  "api_key": "your-api-key-here",
  "model": {
    "id": "custom-model",
    "name": "自定义模型"
  }
}""")
        
        self.json_editor.setText(example)
        
    def update_code_example(self):
        """更新代码示例"""
        example_type = self.example_combo.currentText()
        
        examples = {
            "Python - 基本调用": """import requests
import json

# 配置信息
config = {
    "provider": "deepseek",
    "base_url": "https://api.deepseek.com/v1",
    "api_key": "your-api-key-here",
    "model": "deepseek-chat"
}

# 准备请求
headers = {
    "Authorization": f"Bearer {config['api_key']}",
    "Content-Type": "application/json"
}

data = {
    "model": config["model"],
    "messages": [
        {"role": "user", "content": "你好，请介绍一下你自己"}
    ],
    "temperature": 0.7,
    "max_tokens": 1000
}

# 发送请求
try:
    response = requests.post(
        f"{config['base_url']}/chat/completions",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"回复: {result['choices'][0]['message']['content']}")
    else:
        print(f"请求失败: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"发生错误: {str(e)}")""",
            
            "Python - 流式响应": """import requests
import json

# 流式响应示例
config = {
    "provider": "openai",
    "base_url": "https://api.openai.com/v1",
    "api_key": "your-api-key-here",
    "model": "gpt-4"
}

headers = {
    "Authorization": f"Bearer {config['api_key']}",
    "Content-Type": "application/json"
}

data = {
    "model": config["model"],
    "messages": [
        {"role": "user", "content": "写一个Python函数计算斐波那契数列"}
    ],
    "stream": True,
    "temperature": 0.7
}

# 流式请求
try:
    response = requests.post(
        f"{config['base_url']}/chat/completions",
        headers=headers,
        json=data,
        stream=True
    )
    
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]
                    if data_str != '[DONE]':
                        try:
                            chunk = json.loads(data_str)
                            if 'choices' in chunk and chunk['choices']:
                                delta = chunk['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    print(delta['content'], end='', flush=True)
                        except json.JSONDecodeError:
                            pass
        print()  # 换行
    else:
        print(f"请求失败: {response.status_code}")
        
except Exception as e:
    print(f"发生错误: {str(e)}")""",
            
            "cURL - 命令行调用": """# 基本调用
curl https://api.deepseek.com/v1/chat/completions \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -d '{
    "model": "deepseek-chat",
    "messages": [
      {"role": "user", "content": "你好"}
    ],
    "temperature": 0.7,
    "max_tokens": 1000
  }'

# 流式调用
curl https://api.openai.com/v1/chat/completions \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "写一个Python函数"}
    ],
    "stream": true,
    "temperature": 0.7
  }'"""
        }
        
        code = examples.get(example_type, "# 代码示例加载中...")
        self.code_editor.setText(code)
        
    def format_json(self):
        """格式化JSON"""
        try:
            text = self.json_editor.toPlainText()
            if text.strip():
                data = json.loads(text)
                formatted = json.dumps(data, ensure_ascii=False, indent=2)
                self.json_editor.setText(formatted)
                self.status_label.setText("JSON格式化成功")
            else:
                self.status_label.setText("JSON内容为空")
        except json.JSONDecodeError as e:
            self.status_label.setText(f"JSON格式错误: {str(e)}")
            QMessageBox.warning(self, "JSON错误", f"JSON格式不正确:\n{str(e)}")
            
    def validate_json(self):
        """验证JSON格式"""
        try:
            text = self.json_editor.toPlainText()
            if text.strip():
                json.loads(text)
                self.status_label.setText("✅ JSON格式正确")
                QMessageBox.information(self, "验证通过", "JSON格式正确！")
            else:
                self.status_label.setText("JSON内容为空")
        except json.JSONDecodeError as e:
            self.status_label.setText(f"❌ JSON格式错误")
            QMessageBox.warning(self, "验证失败", f"JSON格式不正确:\n{str(e)}")
            
    def load_json_example(self):
        """加载JSON示例"""
        example = """{
  "provider": "deepseek",
  "base_url": "https://api.deepseek.com/v1",
  "api_key": "sk-your-api-key-here",
  "model": {
    "id": "deepseek-chat",
    "name": "DeepSeek Chat"
  },
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 2000,
    "top_p": 1.0,
    "frequency_penalty": 0,
    "presence_penalty": 0
  },
  "stream": false,
  "timeout": 30
}"""
        self.json_editor.setText(example)
        self.status_label.setText("已加载JSON示例")
        
    def fill_form_example(self):
        """填充表单示例"""
        self.provider_input.setText("deepseek")
        self.base_url_input.setText("https://api.deepseek.com/v1")
        self.api_input.setText("chat/completions")
        self.api_key_input.setText("sk-example-api-key")
        self.model_id_input.setText("deepseek-chat")
        self.model_name_input.setText("DeepSeek Chat")
        self.model_type_combo.setCurrentText("聊天模型")
        
        self.status_label.setText("已填充表单示例")
        
    def clear_form(self):
        """清空表单"""
        self.provider_input.clear()
        self.base_url_input.clear()
        self.api_input.clear()
        self.api_key_input.clear()
        self.model_id_input.clear()
        self.model_name_input.clear()
        self.model_type_combo.setCurrentIndex(0)
        
        self.status_label.setText("表单已清空")
        
    def generate_json_from_form(self):
        """从表单生成JSON"""
        config = {
            "provider": self.provider_input.text() or "custom",
            "base_url": self.base_url_input.text() or "https://api.example.com/v1",
            "api": self.api_input.text() or "chat/completions",
            "api_key": self.api_key_input.text() or "your-api-key-here",
            "model": {
                "id": self.model_id_input.text() or "custom-model",
                "name": self.model_name_input.text() or "自定义模型"
            },
            "model_type": self.model_type_combo.currentText(),
            "created_at": datetime.now().isoformat()
        }
        
        json_str = json.dumps(config, ensure_ascii=False, indent=2)
        self.json_editor.setText(json_str)
        
        self.status_label.setText("已从表单生成JSON")
        
    def copy_code(self):
        """复制代码"""
        import pyperclip
        
        try:
            code = self.code_editor.toPlainText()
            if code:
                pyperclip.copy(code)
                self.status_label.setText("代码已复制到剪贴板")
                QMessageBox.information(self, "复制成功", "代码已复制到剪贴板")
            else:
                QMessageBox.warning(self, "复制失败", "没有可复制的代码")
        except ImportError:
            QMessageBox.warning(self, "复制失败", "需要安装pyperclip库: pip install pyperclip")
        except Exception as e:
            self.status_label.setText(f"复制失败: {str(e)}")
            
    def run_code_test(self):
        """运行代码测试"""
        self.status_label.setText("代码测试功能开发中...")
        QMessageBox.information(self, "代码测试", "代码测试功能正在开发中")
        
    def add_model(self):
        """添加模型"""
        self.status_label.setText("添加模型功能开发中...")
        QMessageBox.information(self, "添加模型", "添加模型功能正在开发中")
        
    def test_connection(self):
        """测试连接"""
        self.status_label.setText("测试连接功能开发中...")
        QMessageBox.information(self, "测试连接", "测试连接功能正在开发中")
        
    def import_config(self):
        """导入配置"""
        self.status_label.setText("导入配置功能开发中...")
        QMessageBox.information(self, "导入配置", "导入配置功能正在开发中")
        
    def export_config(self):
        """导出配置"""
        self.status_label.setText("导出配置功能开发中...")
        QMessageBox.information(self, "导出配置", "导出配置功能正在开发中")
        
    def save_config(self):
        """保存配置"""
        self.status_label.setText("保存配置功能开发中...")
        QMessageBox.information(self, "保存配置", "保存配置功能正在开发中")
        
    def reset_config(self):
        """重置配置"""
        self.json_editor.clear()
        self.clear_form()
        self.status_label.setText("配置已重置")
        
    def validate_config(self):
        """验证配置"""
        self.status_label.setText("验证配置功能开发中...")
        QMessageBox.information(self, "验证配置", "验证配置功能正在开发中")
        
    def update_model_count(self):
        """更新模型计数"""
        # 模拟模型数量
        count = 18  # Coding Plan(6) + 模型API(12)
        self.model_count_label.setText(f"模型数量: {count}")
        
# 测试函数
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = ModelManagerTencent()
    window.setWindowTitle("模型管理 - 腾讯云风格")
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())
