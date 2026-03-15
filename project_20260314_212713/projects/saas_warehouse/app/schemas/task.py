from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models.task import TaskType, TaskStatus


class LocationUpdate(BaseModel):
    """位置更新Schema"""
    latitude: float = Field(..., description="纬度")
    longitude: float = Field(..., description="经度")


class TaskCompleteRequest(BaseModel):
    """任务完成请求Schema"""
    photos: List[str] = Field(..., description="照片URL列表")
    remark: Optional[str] = Field(None, description="备注")


class TaskCreate(BaseModel):
    """任务创建Schema"""
    order_id: str = Field(..., description="订单ID")
    task_type: TaskType = Field(..., description="任务类型")
    assigned_to: str = Field(..., description="执行人ID")


class TaskUpdate(BaseModel):
    """任务更新Schema"""
    assigned_to: Optional[str] = Field(None, description="执行人ID")
    status: Optional[TaskStatus] = Field(None, description="任务状态")


class AttachmentResponse(BaseModel):
    """附件响应Schema"""
    id: str
    file_name: str
    file_url: str
    file_size: Optional[float]
    file_type: Optional[str]
    upload_by: Optional[str]
    create_time: datetime
    
    class Config:
        from_attributes = True


class TaskResponse(BaseModel):
    """任务响应Schema"""
    id: str
    task_no: str
    order_id: str
    task_type: TaskType
    assigned_to: Optional[str]
    status: TaskStatus
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    actual_distance: Optional[float]
    remark: Optional[str]
    attachments: List[AttachmentResponse]
    create_time: datetime
    update_time: datetime
    
    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """任务列表响应Schema"""
    items: List[TaskResponse]
    total: int
    page: int
    size: int
