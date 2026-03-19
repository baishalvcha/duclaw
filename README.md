# 码泓OpenClaw管理器 (Mahong OpenClaw Manager)

## 项目简介

码泓OpenClaw管理器是一款专为OpenClaw设计的可视化管理工具，旨在让复杂的OpenClaw像打开网页QQ一样简单上手，不懂技术也能轻松管理AI助手。

## 版本说明

### 买家版 (Buyer Edition)
- **基础版**：199元，包含基本功能
- **专业版**：399元，包含全部高级功能
- **试用版**：9元/19元（基础/专业），限100套，1个月试用期

### 卖家版 (Seller Edition)
- 内部使用，不对外销售
- 支持许可证码管理
- 支持批量操作

## 功能特性

### 基础功能
- 一键安装/卸载OpenClaw
- 基础模型管理
- 简单配置管理
- 离线激活
- 基础诊断工具
- 状态监控
- 更新检查

### 专业功能（专业版独有）
- 完整模型/通道/代理管理
- 批量操作
- 高级配置
- 智能诊断
- 数据导出
- 性能仪表盘
- 自动化工作流
- 多账户支持

## 系统要求

- Windows 10/11
- Python 3.8+
- OpenClaw 已安装
- 至少4GB内存
- 至少2GB可用磁盘空间

## 快速开始

### 安装
1. 下载最新版本
2. 运行安装程序
3. 按照向导完成安装

### 启动
```bash
cd workspace/买家版
python buyer_main_complete.py
```

### 授权
1. 购买许可证
2. 在软件中输入许可证码
3. 激活对应版本功能

## 项目结构

```
makong/
├── workspace/买家版/           # 买家版完整代码
│   ├── buyer_main_complete.py  # 主程序（完整功能版）
│   ├── buyer_main.py          # 基础版主程序
│   ├── buyer_unified.py       # 统一入口程序
│   ├── auth_manager.py        # 授权管理
│   ├── feature_gate.py        # 功能开关
│   └── dashboard_*.py         # 各种仪表盘
├── OpenClawManager_Buyer_V1.0/ # 买家版V1.0
├── OpenClawManager_GUI/        # GUI版本
├── OpenClawManager_Seller_V1.0/ # 卖家版
└── memory/                    # 项目记忆文件
```

## 开发说明

### 技术栈
- Python 3.8+
- PySide6 (Qt for Python)
- OpenClaw SDK
- MiSans字体

### UI设计
- 深色主题 (#1a1a2e)
- MiSans字体全局应用
- 路由器风格状态指示灯
- 动态标题显示
- 公司logo集成

### 授权系统
- 许可证码验证
- 版本功能控制
- 硬件绑定（计划中）
- 在线激活（计划中）

## 许可证

本项目代码遵循MIT许可证。商业使用需要购买相应许可证。

## 支持

- 基础版：2年免费支持，工作日24小时响应
- 专业版：永久免费支持，优先通道

## 联系方式

- 技术支持：tech@mahong.tech
- 法律事务：leg@mahong.tech
- 官方网站：https://mahong.tech（建设中）

## 更新日志

### 2026-03-19
- 完成买家版UI最终调整
- 优化仪表盘边框颜色
- 调整授权状态图标大小
- 集成MiSans字体
- 添加路由器风格状态指示灯
- 实现动态标题显示
- 集成公司logo

### 2026-03-18
- 创建买家版基础架构
- 实现授权管理系统
- 开发统一入口程序
- 设计多种仪表盘样式

## 贡献

欢迎提交Issue和Pull Request。请确保代码符合项目规范。

## 免责声明

本软件按"原样"提供，不提供任何明示或暗示的担保。使用本软件的风险由用户自行承担。