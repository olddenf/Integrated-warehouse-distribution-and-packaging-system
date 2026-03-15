from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class ApiResponse(BaseModel):
    """统一响应Schema"""
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None
    timestamp: int = int(datetime.now().timestamp() * 1000)


class PaginationParams(BaseModel):
    """分页参数Schema"""
    page: int = 1
    size: int = 20


class IdResponse(BaseModel):
    """ID响应Schema"""
    id: str


class StatusResponse(BaseModel):
    """状态响应Schema"""
    status: str
    message: str
