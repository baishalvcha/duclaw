"""应用配置模块 —— 所有配置从环境变量读取，提供合理的默认值。"""

import os

# ── 数据库 ───────────────────────────────────────────────
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/du_claw",
)

# ── Redis ────────────────────────────────────────────────
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# ── DeepSeek AI ──────────────────────────────────────────
DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# ── 微信小程序 ───────────────────────────────────────────
WECHAT_APPID: str = os.getenv("WECHAT_APPID", "")
WECHAT_SECRET: str = os.getenv("WECHAT_SECRET", "")
WECHAT_TOKEN: str = os.getenv("WECHAT_TOKEN", "")
WECHAT_AES_KEY: str = os.getenv("WECHAT_AES_KEY", "")

# ── 微信支付 ─────────────────────────────────────────────
WECHAT_MCH_ID: str = os.getenv("WECHAT_MCH_ID", "")
WECHAT_PAY_KEY: str = os.getenv("WECHAT_PAY_KEY", "")
WECHAT_NOTIFY_URL: str = os.getenv("WECHAT_NOTIFY_URL", "")

# ── 服务器 ───────────────────────────────────────────────
SERVER_HOST: str = os.getenv("SERVER_HOST", "8.159.152.197")

# ── JWT ─────────────────────────────────────────────────
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "du-claw-secret-key-change-in-production")
JWT_ALGORITHM: str = "HS256"
JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "43200"))  # 默认 30 天