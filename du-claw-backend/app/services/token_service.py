"""Token 计费服务 —— 次数检查、扣减、套餐价格配置。"""

from typing import Dict, Optional
from uuid import UUID

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import RemainCount

# ── 套餐价格配置（单位：分）─────────────────────────────────
PLAN_PRICES: Dict[str, int] = {
    "单次体验": 199,        # 1.99 元
    "10次套餐": 1490,       # 14.90 元
    "30次套餐": 3990,       # 39.90 元
    "月无限": 2990,         # 29.90 元/月
    "日程提醒Pro": 990,     # 9.90 元/月
}

# 套餐对应的次数
PLAN_QUOTA: Dict[str, int] = {
    "单次体验": 1,
    "10次套餐": 10,
    "30次套餐": 30,
    "月无限": 999999,
    "日程提醒Pro": 0,
}

# 场景类型列表
SCENE_TYPES = ["自媒体", "公文", "医学", "营销", "教师"]


class TokenService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_remain(self, user_id: UUID, scene_type: str) -> int:
        """检查用户在指定场景的剩余次数。"""
        stmt = select(RemainCount).where(
            RemainCount.user_id == user_id,
            RemainCount.scene_type == scene_type,
        )
        result = await self.session.execute(stmt)
        remain = result.scalar_one_or_none()
        if remain is None:
            # 首次使用，创建默认记录：赠送 3 次
            remain = RemainCount(
                user_id=user_id,
                scene_type=scene_type,
                remain_count=3,
                total_used=0,
            )
            self.session.add(remain)
            await self.session.commit()
            await self.session.refresh(remain)
            logger.info(
                f"Created default RemainCount for user {user_id}, scene {scene_type}, 3 free tokens"
            )
        return remain.remain_count

    async def deduct(self, user_id: UUID, scene_type: str) -> bool:
        """扣减一次使用次数，返回是否扣减成功。"""
        stmt = select(RemainCount).where(
            RemainCount.user_id == user_id,
            RemainCount.scene_type == scene_type,
        )
        result = await self.session.execute(stmt)
        remain = result.scalar_one_or_none()
        if remain is None:
            # 无记录则创建后扣减
            await self.check_remain(user_id, scene_type)
            result2 = await self.session.execute(stmt)
            remain = result2.scalar_one()

        if remain.remain_count <= 0:
            logger.warning(
                f"User {user_id} no remain count for scene {scene_type}"
            )
            return False

        remain.remain_count -= 1
        remain.total_used += 1
        await self.session.commit()
        logger.info(
            f"Deducted 1 token for user {user_id}, scene {scene_type}, "
            f"remain {remain.remain_count}"
        )
        return True

    async def add_quota(
        self, user_id: UUID, scene_type: str, count: int
    ) -> None:
        """增加指定场景的剩余次数（订单支付成功后调用）。"""
        stmt = select(RemainCount).where(
            RemainCount.user_id == user_id,
            RemainCount.scene_type == scene_type,
        )
        result = await self.session.execute(stmt)
        remain = result.scalar_one_or_none()
        if remain is None:
            remain = RemainCount(
                user_id=user_id,
                scene_type=scene_type,
                remain_count=count,
                total_used=0,
            )
            self.session.add(remain)
        else:
            remain.remain_count += count

        await self.session.commit()
        logger.info(
            f"Added {count} quota for user {user_id}, scene {scene_type}"
        )