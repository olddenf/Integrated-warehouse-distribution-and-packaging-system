from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.common import ApiResponse
from app.services.report_service import ReportService
from app.core.database import get_db
from app.core.deps import require_role
from app.models.user import User, UserRole


router = APIRouter(prefix="/reports", tags=["报表"])


@router.get("/order", response_model=ApiResponse)
async def get_order_report(
    start_date: str,
    end_date: str,
    group_by: str = "day",
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.DISPATCHER)),
    db: AsyncSession = Depends(get_db)
):
    """订单报表"""
    service = ReportService(db)
    report = await service.get_order_report(start_date, end_date, group_by)
    return ApiResponse(data=report)


@router.get("/worker", response_model=ApiResponse)
async def get_worker_report(
    start_date: str,
    end_date: str,
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.DISPATCHER)),
    db: AsyncSession = Depends(get_db)
):
    """人员工作量报表"""
    service = ReportService(db)
    report = await service.get_worker_report(start_date, end_date)
    return ApiResponse(data=report)


@router.get("/fee", response_model=ApiResponse)
async def get_fee_report(
    start_date: str,
    end_date: str,
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.DISPATCHER)),
    db: AsyncSession = Depends(get_db)
):
    """费用报表"""
    service = ReportService(db)
    report = await service.get_fee_report(start_date, end_date)
    return ApiResponse(data=report)


@router.post("/export", response_model=ApiResponse)
async def export_report(
    report_type: str,
    start_date: str,
    end_date: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.DISPATCHER)),
    db: AsyncSession = Depends(get_db)
):
    """导出报表"""
    service = ReportService(db)
    report_id = await service.create_export_task(report_type, start_date, end_date)
    return ApiResponse(data={"report_id": report_id, "status": "generating"})
