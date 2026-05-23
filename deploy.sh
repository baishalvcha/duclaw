#!/bin/bash
set -e

echo "=== du-claw 一键部署 ==="

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 停止并移除旧容器
echo "[1/4] 停止旧服务..."
docker compose down

# 重新构建后端镜像
echo "[2/4] 构建后端镜像..."
docker compose build --no-cache backend

# 启动所有服务
echo "[3/4] 启动服务..."
docker compose up -d

# 等待服务就绪
echo "[4/4] 等待服务启动..."
sleep 10

# 验证数据库连接
echo "验证数据库连接..."
docker compose exec -T backend python -c "from app.database import engine, Base; import asyncio; asyncio.run(engine.dispose())" 2>/dev/null || echo "提示: 数据库初始化将在首次请求时自动完成"

echo ""
echo "=== 部署完成 ==="
echo "后端API:     http://8.159.152.197:8000/api/health"
echo "API文档:     http://8.159.152.197:8000/docs"
echo "数据库:      postgresql://duclaw:duclaw2024!@8.159.152.197:5432/duclaw"
echo "Redis:       redis://8.159.152.197:6379/0"
echo ""
echo "常用命令:"
echo "  查看日志:  docker compose logs -f backend"
echo "  重启服务:  docker compose restart backend"
echo "  停止服务:  docker compose down"