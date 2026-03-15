from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date
from app.schemas.task import TaskCompleteRequest, LocationUpdate, TaskResponse
from app.schemas.common import ApiResponse
from app.services.task_service import TaskService
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User


router = APIRouter(prefix="/tasks", tags=["任务"])


@router.get("/my-tasks", response_model=ApiResponse)
async def get_my_tasks(
    task_type: Optional[str] = None,
    date: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """我的任务列表"""
    service = TaskService(db)
    
    # 解析日期
    target_date = date.fromisoformat(date) if date else None
    
    tasks = await service.get_my_tasks(
        worker_id=current_user.id,
        task_type=task_type,
        date=target_date
    )
    
    return ApiResponse(data=tasks)


@router.get("/{task_id}", response_model=ApiResponse)
async def get_task_detail(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """任务详情"""
    service = TaskService(db)
    task = await service.get_task_detail(task_id, current_user.id)
    return ApiResponse(data=TaskResponse.model_validate(task))


@router.post("/{task_id}/start", response_model=ApiResponse)
async def start_task(
    task_id: str,
    location: LocationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """开始任务"""
    service = TaskService(db)
    task = await service.start_task(task_id, location, current_user.id)
    return ApiResponse(data=TaskResponse.model_validate(task))


@router.post("/{task_id}/complete", response_model=ApiResponse)
async def complete_task(
    task_id: str,
    data: TaskCompleteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """完成任务"""
    service = TaskService(db)
    task = await service.complete_task(task_id, data, current_user.id)
    return ApiResponse(data=TaskResponse.model_validate(task))


@router.post("/{task_id}/upload", response_model=ApiResponse)
async def upload_photo(
    task_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """上传照片"""
    # 这里简化处理，实际应该上传到OSS
    file_url = f"https://example.com/{file.filename}"
    return ApiResponse(data={"file_url": file_url})
