#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语言管理模块
"""

class LanguageManager:
    """语言管理器"""
    
    def __init__(self):
        self.current_language = "zh"
        self.translations = {
            "zh": {
                "window_title": "码泓mahong-openclaw管理器-买家版V1.0",
                "nav_home": "🏠 首页",
                "nav_auth": "🔑 授权信息",
                "nav_install": "🚀 安装/卸载",
                "nav_model": "🤖 模型管理",
                "nav_channel": "📱 通道管理",
                "nav_agent": "👥 Agent管理",
                "nav_settings": "⚙️ 设置",
                "nav_help": "🆘 帮助",
                "mode_seller": "卖家模式",
                "mode_buyer": "买家模式",
                "mode_switch": "模式切换",
                "nav_taobao": "🛒 淘宝发货",
                "nav_baidu": "☁️ 百度云",
                "seller_title": "卖家版功能",
                "buyer_title": "买家版功能",
                "menu_file": "文件",
                "menu_exit": "退出",
                "menu_tool": "工具",
                "menu_config": "配置OpenClaw",
                "menu_restart": "重启服务",
                "menu_clear_cache": "清理缓存",
                "menu_help": "帮助",
                "menu_about": "关于",
                "menu_usage_help": "使用帮助",
                "tray_show": "显示窗口",
                "tray_exit": "退出",
                "install_title": "安装OpenClaw",
                "install_path": "安装路径:",
                "install_browse": "浏览",
                "install_mirror": "镜像源:",
                "install_start": "开始安装",
                "uninstall_title": "卸载OpenClaw",
                "uninstall_path": "卸载路径:",
                "uninstall_start": "开始卸载",
                "model_add": "添加AI模型",
                "model_name": "模型名称:",
                "model_provider": "提供商:",
                "model_api_key": "API Key:",
                "model_base_url": "Base URL:",
                "model_add_btn": "添加模型",
                "model_list": "模型列表",
                "model_test": "测试连接",
                "model_delete": "删除模型",
                "channel_tool": "通道配置工具",
                "channel_launch": "启动通道配置工具",
                "channel_view": "查看当前配置",
                "channel_info": "通道类型说明",
                "agent_create": "创建Agent",
                "agent_name": "Agent名称:",
                "agent_type": "Agent类型:",
                "agent_create_btn": "创建",
                "agent_list": "Agent列表",
                "agent_manage": "管理Agent",
                "settings_general": "通用设置",
                "settings_startup": "开机自启动",
                "settings_tray": "最小化到托盘",
                "settings_update": "更新设置",
                "settings_auto_update": "自动检查更新",
                "settings_check_update": "立即检查更新",
                "settings_language": "语言设置",
                "settings_interface_lang": "界面语言:",
                "settings_save": "保存设置",
                "help_usage": "使用说明",
                "help_faq": "常见问题",
                "help_support": "技术支持",
                "about_title": "关于",
                "about_content": "码泓mahong-OpenClaw管理器 v2.0\n\n一款一键安装/绿化版的OpenClaw可视化管理工具\n面向非技术用户，提供图形化操作界面\n支持卖家版和买家版模式切换\n\n© 2026 码泓 mahong 版权所有\n版本：v2.0 (2026-03-18)\n官方网站：https://mahong.openclaw.ai"
            },
            "en": {
                "window_title": "mahong-OpenClaw Manager v2.0 © 2026",
                "nav_home": "🏠 Home",
                "nav_auth": "🔑 Authorization",
                "nav_install": "🚀 Install/Uninstall",
                "nav_model": "🤖 Model Management",
                "nav_channel": "📱 Channel Management",
                "nav_agent": "👥 Agent Management",
                "nav_settings": "⚙️ Settings",
                "nav_help": "🆘 Help",
                "mode_seller": "Seller Mode",
                "mode_buyer": "Buyer Mode",
                "mode_switch": "Mode Switch",
                "nav_taobao": "🛒 Taobao Delivery",
                "nav_baidu": "☁️ Baidu Cloud",
                "seller_title": "Seller Features",
                "buyer_title": "Buyer Features",
                "menu_file": "File",
                "menu_exit": "Exit",
                "menu_tool": "Tools",
                "menu_config": "Configure OpenClaw",
                "menu_restart": "Restart Service",
                "menu_clear_cache": "Clear Cache",
                "menu_help": "Help",
                "menu_about": "About",
                "menu_usage_help": "Usage Help",
                "tray_show": "Show Window",
                "tray_exit": "Exit",
                "install_title": "Install OpenClaw",
                "install_path": "Install Path:",
                "install_browse": "Browse",
                "install_mirror": "Mirror:",
                "install_start": "Start Install",
                "uninstall_title": "Uninstall OpenClaw",
                "uninstall_path": "Uninstall Path:",
                "uninstall_start": "Start Uninstall",
                "model_add": "Add AI Model",
                "model_name": "Model Name:",
                "model_provider": "Provider:",
                "model_api_key": "API Key:",
                "model_base_url": "Base URL:",
                "model_add_btn": "Add Model",
                "model_list": "Model List",
                "model_test": "Test Connection",
                "model_delete": "Delete Model",
                "channel_tool": "Channel Configuration Tool",
                "channel_launch": "Launch Config Tool",
                "channel_view": "View Current Config",
                "channel_info": "Channel Type Description",
                "agent_create": "Create Agent",
                "agent_name": "Agent Name:",
                "agent_type": "Agent Type:",
                "agent_create_btn": "Create",
                "agent_list": "Agent List",
                "agent_manage": "Manage Agent",
                "settings_general": "General Settings",
                "settings_startup": "Run on Startup",
                "settings_tray": "Minimize to Tray",
                "settings_update": "Update Settings",
                "settings_auto_update": "Auto Check Updates",
                "settings_check_update": "Check Updates Now",
                "settings_language": "Language Settings",
                "settings_interface_lang": "Interface Language:",
                "settings_save": "Save Settings",
                "help_usage": "Usage Instructions",
                "help_faq": "FAQ",
                "help_support": "Technical Support",
                "about_title": "About",
                "about_content": "mahong-OpenClaw Manager v2.0\n\nA one-click installation/green version of OpenClaw visualization management tool\nFor non-technical users, providing a graphical operation interface\nSupports seller and buyer mode switching\n\n© 2026 mahong All Rights Reserved\nVersion: v2.0 (2026-03-18)\nOfficial Website: https://mahong.openclaw.ai"
            }
        }
    
    def set_language(self, lang):
        """设置语言"""
        if lang in self.translations:
            self.current_language = lang
    
    def get(self, key):
        """获取翻译"""
        lang_translations = self.translations.get(self.current_language, {})
        return lang_translations.get(key, key)
    
    def get_languages(self):
        """获取支持的语言列表"""
        return list(self.translations.keys())


# 创建全局语言管理器实例
language_manager = LanguageManager()