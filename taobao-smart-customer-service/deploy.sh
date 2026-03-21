#!/bin/bash

echo "开始部署淘宝客服智能接入系统..."

# 1. 检查Python环境
echo "检查Python环境..."
python --version
pip --version

# 2. 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 3. 初始化数据库
echo "初始化数据库..."
python scripts/init_db.py

# 4. 启动服务
echo "启动服务..."
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4

echo "部署完成！"
