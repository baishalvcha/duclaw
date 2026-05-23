"""Pydantic Schemas — 订单。"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class OrderCreate(BaseModel):
    """创建订单。"""
    plan_type: str
    amount: int


class OrderResponse(BaseModel):
    """订单响应。"""
    id: UUID
    user_id: UUID
    plan_type: str
    amount: int
    status: str
    transaction_id: Optional[str] = None
    created_at: datetime
    paid_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PaymentCallback(BaseModel):
    """微信支付回调数据。"""
    appid: str
    mch_id: str
    out_trade_no: str
    transaction_id: str
    total_fee: int
    time_end: str
    openid: str
    sign: str