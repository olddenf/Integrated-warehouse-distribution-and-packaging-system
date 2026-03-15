from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from app.models.task import TaskType


class AutoDispatchRequest(BaseModel):
    """智能排单请求Schema"""
    order_ids: List[str] = Field(..., description="订单ID列表")
    task_type: TaskType = Field(..., description="任务类型")
    dispatch_date: date = Field(..., description="派单日期")


class ManualDispatchRequest(BaseModel):
    """手动调整请求Schema"""
    task_id: str = Field(..., description="任务ID")
    new_worker_id: str = Field(..., description="新执行人ID")
    reason: str = Field(..., description="调整原因")


class DispatchResult(BaseModel):
    """排单结果Schema"""
    order_id: str
    success: bool
    task_id: Optional[str] = None
    task_no: Optional[str] = None
    worker_name: Optional[str] = None
    worker_phone: Optional[str] = None
    score: Optional[float] = None
    score_details: Optional[List[str]] = None
    reason: Optional[str] = None


class DispatchResponse(BaseModel):
    """排单响应Schema"""
    results: List[DispatchResult]
