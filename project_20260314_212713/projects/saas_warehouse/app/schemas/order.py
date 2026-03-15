from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from app.models.order import OrderStatus


class OrderProductCreate(BaseModel):
    """订单商品创建Schema"""
    product_name: str = Field(..., description="商品名称")
    product_code: Optional[str] = Field(None, description="商品编码")
    quantity: float = Field(..., gt=0, description="数量")
    unit: str = Field(..., description="单位")


class OrderCreate(BaseModel):
    """订单创建Schema"""
    customer_name: str = Field(..., min_length=1, max_length=50, description="客户姓名")
    customer_phone: str = Field(..., pattern=r"^1[3-9]\d{9}$", description="客户电话")
    address: str = Field(..., min_length=5, max_length=255, description="配送地址")
    appointment_time: datetime = Field(..., description="预约时间")
    products: List[OrderProductCreate] = Field(..., min_items=1, description="商品列表")
    remark: Optional[str] = Field(None, max_length=500, description="备注")
    
    @validator('appointment_time')
    def validate_appointment_time(cls, v):
        """预约时间必须在未来"""
        if v < datetime.now():
            raise ValueError('预约时间必须在未来')
        return v


class OrderUpdate(BaseModel):
    """订单更新Schema"""
    customer_name: Optional[str] = Field(None, min_length=1, max_length=50, description="客户姓名")
    customer_phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$", description="客户电话")
    address: Optional[str] = Field(None, min_length=5, max_length=255, description="配送地址")
    appointment_time: Optional[datetime] = Field(None, description="预约时间")
    remark: Optional[str] = Field(None, max_length=500, description="备注")


class OrderProductResponse(BaseModel):
    """订单商品响应Schema"""
    id: str
    product_name: str
    product_code: Optional[str]
    quantity: float
    unit: str
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """订单响应Schema"""
    id: str
    order_no: str
    customer_name: str
    customer_phone: str
    address: str
    latitude: Optional[float]
    longitude: Optional[float]
    appointment_time: datetime
    status: OrderStatus
    total_amount: float
    remark: Optional[str]
    products: List[OrderProductResponse]
    create_time: datetime
    update_time: datetime
    
    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """订单列表响应Schema"""
    items: List[OrderResponse]
    total: int
    page: int
    size: int
