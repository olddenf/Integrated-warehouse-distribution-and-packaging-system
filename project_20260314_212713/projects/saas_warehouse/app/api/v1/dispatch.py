from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.dispatch import AutoDispatchRequest, ManualDispatchRequest, DispatchResponse
from app.schemas.common import ApiResponse
from app.services.dispatch_service import DispatchService
from app.core.database import get_db
from app.core.deps import require_role
from app.models.user import User, UserRole


router = APIRouter(prefix="/dispatch", tags=["调度"])


@router.post("/auto", response_model=ApiResponse)
async def auto_dispatch(
    data: AutoDispatchRequest,
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.DISPATCHER)),
    db: AsyncSession = Depends(get_db)
):
    """智能排单"""
    service = DispatchService(db)
    results = await service.auto_dispatch(
        order_ids=data.order_ids,
        task_type=data.task_type,
        dispatch_date=data.dispatch_date
    )
    return ApiResponse(data={"results": results})


@router.post("/manual", response_model=ApiResponse)
async def manual_dispatch(
    data: ManualDispatchRequest,
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.DISPATCHER)),
    db: AsyncSession = Depends(get_db)
):
    """手动调整"""
    service = DispatchService(db)
    task = await service.manual_dispatch(
        task_id=data.task_id,
        new_worker_id=data.new_worker_id,
        reason=data.reason,
        operator_id=current_user.id
    )
    return ApiResponse(data={"task_id": task.id, "status": task.status.value})
