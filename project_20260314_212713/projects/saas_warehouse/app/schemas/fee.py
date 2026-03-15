from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models.fee import FeeType, FeeStatus


class FeeCreate(BaseModel):
    """费用创建Schema"""
    order_id: str = Field(..., description="订单ID")
    fee_type: FeeType = Field(..., description="费用类型")
    amount: float = Field(..., gt=0, description="金额")
    description: Optional[str] = Field(None, description="描述")


class FeeUpdate(BaseModel):
    """费用更新Schema"""
    amount: float = Field(..., gt=0, description="金额")
    description: Optional[str] = Field(None, description="描述")


class FeeAdjustRequest(BaseModel):
    """费用调整请求Schema"""
    new_amount: float = Field(..., gt=0, description="新金额")
    reason: str = Field(..., description="调整原因")


class FeeResponse(BaseModel):
    """费用响应Schema"""
    id: str
    order_id: str
    fee_type: FeeType
    amount: float
    description: Optional[str]
    status: FeeStatus
    create_time: datetime
    update_time: datetime
    
    class Config:
        from_attributes = True


class FeeListResponse(BaseModel):
    """费用列表响应Schema"""
    items: List[FeeResponse]
    total: int
    page: int
    size: int
