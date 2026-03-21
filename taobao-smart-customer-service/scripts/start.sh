#!/bin/bash
# 启动服务脚本

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
