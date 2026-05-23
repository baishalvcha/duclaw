# du-claw 个人 AI 助手

## 项目简介

du-claw 是一款基于 AI 的个人智能助手小程序，提供智能对话、文件管理、知识库等功能。用户可以通过微信小程序随时随地与 AI 助手交互，获取高效、便捷的智能服务。

## 技术架构

| 层级 | 技术栈 |
|------|--------|
| **后端框架** | FastAPI (Python 3.11) |
| **数据库** | PostgreSQL 15 |
| **缓存** | Redis 7 |
| **AI 模型** | DeepSeek API |
| **容器化** | Docker + Docker Compose |
| **反向代理** | Nginx |
| **客户端** | 微信小程序 |

## 快速开始

### 环境要求

- Docker >= 20.10
- Docker Compose >= 2.0
- 服务器：Linux（推荐 Ubuntu 22.04），已开放 8000 / 80 / 5432 / 6379 端口

### 部署步骤

1. 将项目上传至服务器

```bash
scp -r du-claw-backend docker-compose.yml nginx/ deploy.sh root@8.159.152.197:/data/du-claw/
```

2. 配置环境变量

```bash
cp du-claw-backend/.env.example du-claw-backend/.env
# 编辑 .env，填入真实的 API Key、微信小程序 AppID 等
vim du-claw-backend/.env
```

3. 执行一键部署

```bash
chmod +x deploy.sh
./deploy.sh
```

4. 验证服务

```bash
curl http://8.159.152.197:8000/api/health
```

## 目录结构

```
du-claw/
├── du-claw-backend/           # 后端服务
│   ├── Dockerfile             # 后端容器构建文件
│   ├── .env.example           # 环境变量模板
│   └── app/                   # FastAPI 应用代码
│       ├── main.py            # 应用入口
│       ├── database.py        # 数据库连接配置
│       ├── models/             # 数据模型
│       ├── routers/            # API 路由
│       ├── services/           # 业务逻辑
│       └── core/               # 核心配置
├── nginx/
│   └── nginx.conf             # Nginx 配置
├── docker-compose.yml         # 容器编排
├── deploy.sh                  # 一键部署脚本
└── README.md                  # 项目文档
```

## API 文档

服务启动后，访问 Swagger UI 查看完整 API 文档：

```
http://8.159.152.197:8000/docs
```

## 环境变量配置说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `DATABASE_URL` | PostgreSQL 连接串 | `postgresql+asyncpg://duclaw:password@db:5432/duclaw` |
| `REDIS_URL` | Redis 连接串 | `redis://redis:6379/0` |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | `sk-xxx` |
| `DEEPSEEK_BASE_URL` | DeepSeek API 地址 | `https://api.deepseek.com` |
| `WECHAT_APPID` | 微信小程序 AppID | `wx_xxx` |
| `WECHAT_SECRET` | 微信小程序 Secret | - |
| `WECHAT_TOKEN` | 微信消息校验 Token | - |
| `WECHAT_AES_KEY` | 微信消息加解密密钥 | - |
| `SERVER_HOST` | 服务器公网 IP | `8.159.152.197` |
| `JWT_SECRET` | JWT 签名密钥 | 随机字符串 |
| `JWT_ALGORITHM` | JWT 签名算法 | `HS256` |

## 小程序配置说明

1. 在[微信公众平台](https://mp.weixin.qq.com/)注册小程序，获取 AppID 和 Secret
2. 配置服务器域名白名单：`https://8.159.152.197`
3. 在 `project.config.json` 中配置 AppID
4. 配置小程序 request 合法域名：`https://8.159.152.197`
5. 开发工具中预览 / 上传代码并提交审核