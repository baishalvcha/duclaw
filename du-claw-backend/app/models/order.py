"""订单模型。"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    plan_type = Column(
        String(30),
        nullable=False,
        comment="单次体验 / 10次套餐 / 30次套餐 / 月无限 / 日程提醒Pro",
    )
    amount = Column(Integer, nullable=False, comment="金额，单位：分")
    status = Column(
        String(20), nullable=False, default="pending", comment="pending / paid / cancelled"
    )
    transaction_id = Column(String(64), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    paid_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="orders")