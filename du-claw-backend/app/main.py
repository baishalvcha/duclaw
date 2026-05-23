"""FastAPI 主入口 —— 创建 app，配置 CORS，注册路由，启动定时任务。"""

import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.database import Base, engine
from app.routers import user, chat, schedule, order
from app.scheduler import start_scheduler, stop_scheduler


# ── 配置 loguru ──────────────────────────────────────────────
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
)


# ── Lifespan 管理 ────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """启动时初始化数据库表，启动定时任务；关闭时停止定时任务。"""
    logger.info("Starting up...")
    # 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")

    # 启动定时任务
    start_scheduler()

    yield

    logger.info("Shutting down...")
    # 停止定时任务
    stop_scheduler()
    logger.info("Scheduler stopped")


# ── 创建 FastAPI 应用 ────────────────────────────────────────
app = FastAPI(
    title="du-claw 个人 AI 助手后端",
    description="基于 FastAPI + PostgreSQL + DeepSeek API 的智能写作与日程管理平台",
    version="1.0.0",
    lifespan=lifespan,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(schedule.router)
app.include_router(order.router)


# ── 健康检查端点 ──────────────────────────────────────────────
@app.get("/api/health")
async def health_check():
    """健康检查端点，用于服务探活。"""
    return {
        "status": "healthy",
        "service": "du-claw-backend",
        "version": "1.0.0",
    }


# ── 根路径 ───────────────────────────────────────────────────
@app.get("/")
async def root():
    """根路径，返回 API 信息。"""
    return {
        "message": "欢迎使用 du-claw 个人 AI 助手后端 API",
        "docs": "/docs",
        "redoc": "/redoc",
    }


# ── 主入口 ───────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)