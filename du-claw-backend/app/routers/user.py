"""用户路由 —— 微信登录、获取用户信息、剩余次数查询。"""

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from app.database import get_db
from app.config import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET_KEY
from app.middleware.auth import get_current_user_id
from app.models.user import User, RemainCount
from app.schemas.user import (
    LoginResponse,
    RemainCountResponse,
    UserCreate,
    UserResponse,
)
from app.services.wechat_service import wechat_service

router = APIRouter(prefix="/api/user", tags=["用户"])


def _create_token(user_id: str) -> str:
    """生成 JWT token。"""
    from datetime import datetime, timedelta, timezone

    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {
        "user_id": user_id,
        "exp": expire,
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


@router.post("/login", response_model=LoginResponse)
async def login(req: UserCreate, db: AsyncSession = Depends(get_db)):
    """微信登录：code 换 openid，创建或返回用户 + JWT token。"""
    try:
        wx_data = await wechat_service.code2session(req.code)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    openid = wx_data["openid"]
    unionid = wx_data.get("unionid")

    # 查找或创建用户
    stmt = select(User).where(User.openid == openid)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            openid=openid,
            unionid=unionid,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"New user created: {user.id}, openid={openid}")
    elif unionid and not user.unionid:
        user.unionid = unionid
        await db.commit()
        await db.refresh(user)

    token = _create_token(str(user.id))
    return LoginResponse(user=UserResponse.model_validate(user), token=token)


@router.get("/profile", response_model=UserResponse)
async def get_profile(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取当前用户信息。"""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在"
        )
    return UserResponse.model_validate(user)


@router.get("/remain", response_model=list[RemainCountResponse])
async def get_remain(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取当前用户各场景的剩余次数。"""
    from app.services.token_service import SCENE_TYPES, TokenService

    token_svc = TokenService(db)
    results = []
    for scene in SCENE_TYPES:
        remain_count = await token_svc.check_remain(user_id, scene)
        stmt = select(RemainCount).where(
            RemainCount.user_id == user_id,
            RemainCount.scene_type == scene,
        )
        result = await db.execute(stmt)
        rc = result.scalar_one_or_none()
        results.append(
            RemainCountResponse(
                scene_type=scene,
                remain_count=remain_count,
                total_used=rc.total_used if rc else 0,
            )
        )
    return results