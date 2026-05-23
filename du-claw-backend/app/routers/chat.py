"""对话路由 —— AI 对话核心接口。"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user_id
from app.models.conversation import Conversation, Message
from app.schemas.conversation import (
    ChatRequest,
    ChatResponse,
    ConversationResponse,
    MessageResponse,
)
from app.services.ai_service import ai_service
from app.services.token_service import SCENE_TYPES, TokenService

router = APIRouter(prefix="/api/chat", tags=["对话"])


@router.post("/send", response_model=ChatResponse)
async def send_message(
    req: ChatRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """发送消息，调用 AI 并返回回复。需认证，扣减次数。"""
    # 校验场景类型
    if req.scene_type not in SCENE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持场景类型: {req.scene_type}，可选: {SCENE_TYPES}",
        )

    # 扣减次数
    token_svc = TokenService(db)
    can_deduct = await token_svc.deduct(user_id, req.scene_type)
    if not can_deduct:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="剩余次数不足，请购买套餐",
        )

    # 查找或创建对话
    if req.conversation_id:
        stmt = select(Conversation).where(
            Conversation.id == req.conversation_id,
            Conversation.user_id == user_id,
        )
        result = await db.execute(stmt)
        conv = result.scalar_one_or_none()
        if conv is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="对话不存在"
            )
    else:
        conv = Conversation(
            user_id=user_id,
            scene_type=req.scene_type,
            title=req.message[:50],
        )
        db.add(conv)
        await db.commit()
        await db.refresh(conv)

    # 保存用户消息
    user_msg = Message(
        conversation_id=conv.id,
        role="user",
        content=req.message,
        token_count=0,
    )
    db.add(user_msg)

    # 调用 AI
    try:
        # 将 conversation_id 注入 request
        req.conversation_id = conv.id
        reply, _, token_used = await ai_service.chat(req, user_id)
    except RuntimeError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )

    # 保存 AI 回复
    assistant_msg = Message(
        conversation_id=conv.id,
        role="assistant",
        content=reply,
        token_count=token_used,
    )
    db.add(assistant_msg)

    # 更新对话时间
    from datetime import datetime, timezone
    conv.updated_at = datetime.now(timezone.utc)

    await db.commit()

    logger.info(
        f"Message sent: conv={conv.id}, user={user_id}, "
        f"scene={req.scene_type}, tokens={token_used}"
    )
    return ChatResponse(reply=reply, conversation_id=conv.id, token_used=token_used)


@router.get("/conversations", response_model=list[ConversationResponse])
async def list_conversations(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取当前用户的对话列表。"""
    # 子查询获取每个对话的消息数量
    stmt = (
        select(
            Conversation,
            func.count(Message.id).label("message_count"),
        )
        .outerjoin(Message, Message.conversation_id == Conversation.id)
        .where(Conversation.user_id == user_id)
        .group_by(Conversation.id)
        .order_by(Conversation.updated_at.desc())
    )
    result = await db.execute(stmt)
    rows = result.all()

    return [
        ConversationResponse(
            id=conv.id,
            user_id=conv.user_id,
            scene_type=conv.scene_type,
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=count,
        )
        for conv, count in rows
    ]


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
async def get_messages(
    conversation_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取指定对话的所有消息。"""
    # 先确认对话属于当前用户
    conv_stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id,
    )
    result = await db.execute(conv_stmt)
    if result.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="对话不存在"
        )

    stmt = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    result = await db.execute(stmt)
    messages = result.scalars().all()
    return [MessageResponse.model_validate(m) for m in messages]


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """删除指定对话及其所有消息。"""
    stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id,
    )
    result = await db.execute(stmt)
    conv = result.scalar_one_or_none()
    if conv is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="对话不存在"
        )

    await db.delete(conv)
    await db.commit()
    logger.info(f"Conversation {conversation_id} deleted by user {user_id}")
    return {"detail": "对话已删除"}