from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    """用户基础Schema"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    name: str = Field(..., min_length=1, max_length=50, description="姓名")
    phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$", description="手机号")
    role: UserRole = Field(..., description="角色")


class UserCreate(UserBase):
    """创建用户Schema"""
    password: str = Field(..., min_length=6, description="密码")


class UserUpdate(BaseModel):
    """更新用户Schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="姓名")
    phone: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$", description="手机号")
    status: Optional[bool] = Field(None, description="状态")


class UserResponse(UserBase):
    """用户响应Schema"""
    id: str
    status: bool
    create_time: datetime
    update_time: datetime
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """登录请求Schema"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class LoginResponse(BaseModel):
    """登录响应Schema"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
