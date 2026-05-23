"""日程路由 —— CRUD 操作，全部需认证。"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user_id
from app.schemas.schedule import ScheduleCreate, ScheduleResponse, ScheduleUpdate
from app.services.schedule_service import ScheduleService

router = APIRouter(prefix="/api/schedule", tags=["日程"])


@router.post("", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    req: ScheduleCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """创建新日程。"""
    svc = ScheduleService(db)
    schedule = await svc.create_schedule(
        user_id=user_id,
        title=req.title,
        description=req.description,
        remind_time=req.remind_time,
    )
    return ScheduleResponse.model_validate(schedule)


@router.get("/today", response_model=list[ScheduleResponse])
async def get_today_schedules(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取今日日程。"""
    svc = ScheduleService(db)
    schedules = await svc.get_today_schedules(user_id)
    return [ScheduleResponse.model_validate(s) for s in schedules]


@router.get("/all", response_model=list[ScheduleResponse])
async def get_all_schedules(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """获取所有日程。"""
    svc = ScheduleService(db)
    schedules = await svc.get_all_schedules(user_id)
    return [ScheduleResponse.model_validate(s) for s in schedules]


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: UUID,
    req: ScheduleUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """更新日程（部分字段）。"""
    from sqlalchemy import select
    from app.models.schedule import Schedule

    stmt = select(Schedule).where(
        Schedule.id == schedule_id, Schedule.user_id == user_id
    )
    result = await db.execute(stmt)
    schedule = result.scalar_one_or_none()
    if schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="日程不存在"
        )

    update_data = req.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(schedule, field, value)

    await db.commit()
    await db.refresh(schedule)
    return ScheduleResponse.model_validate(schedule)


@router.delete("/{schedule_id}")
async def delete_schedule(
    schedule_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """删除日程。"""
    svc = ScheduleService(db)
    success = await svc.delete_schedule(schedule_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="日程不存在"
        )
    return {"detail": "日程已删除"}