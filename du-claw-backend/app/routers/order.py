"""订单路由 —— 创建订单、支付回调处理。"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user_id
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderResponse
from app.services.token_service import PLAN_PRICES, PLAN_QUOTA, SCENE_TYPES, TokenService
from app.services.wechat_service import wechat_service

router = APIRouter(prefix="/api/order", tags=["订单"])


@router.post("/create", response_model=OrderResponse)
async def create_order(
    req: OrderCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """创建订单并返回微信支付参数。"""
    if req.plan_type not in PLAN_PRICES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效套餐类型: {req.plan_type}",
        )

    amount = PLAN_PRICES[req.plan_type]
    out_trade_no = f"DC{int(uuid.uuid4().hex[:16], 16)}"[:32]

    order = Order(
        user_id=user_id,
        plan_type=req.plan_type,
        amount=amount,
        status="pending",
        transaction_id=out_trade_no,
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)

    logger.info(f"Order created: {order.id}, plan={req.plan_type}, amount={amount}")

    # 返回支付参数（实际需要调用统一下单，这里返回订单信息）
    return OrderResponse.model_validate(order)


@router.post("/callback")
async def payment_callback(request: Request, db: AsyncSession = Depends(get_db)):
    """微信支付回调通知。"""
    try:
        body = await request.body()
        data = await request.form()
        callback_data = dict(data)

        # 验证签名
        if not wechat_service.verify_callback_sign(callback_data):
            logger.error("Payment callback signature verification failed")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="签名验证失败"
            )

        out_trade_no = callback_data.get("out_trade_no")
        transaction_id = callback_data.get("transaction_id")

        # 更新订单状态
        from sqlalchemy import select
        from datetime import datetime, timezone

        stmt = select(Order).where(Order.transaction_id == out_trade_no)
        result = await db.execute(stmt)
        order = result.scalar_one_or_none()

        if order is None:
            logger.error(f"Order not found: {out_trade_no}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="订单不存在"
            )

        order.status = "paid"
        order.paid_at = datetime.now(timezone.utc)

        # 增加使用次数
        quota = PLAN_QUOTA.get(order.plan_type, 0)
        if quota > 0:
            token_svc = TokenService(db)
            for scene in SCENE_TYPES:
                await token_svc.add_quota(order.user_id, scene, quota)

        await db.commit()
        logger.info(
            f"Order {out_trade_no} paid, transaction={transaction_id}, "
            f"quota added: {quota}"
        )

        # 返回成功通知给微信
        return {"code": "SUCCESS", "message": "OK"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Payment callback error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"支付回调处理失败: {str(e)}",
        )