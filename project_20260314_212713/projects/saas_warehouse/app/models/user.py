from sqlalchemy import Column, String, Enum, Boolean, DateTime, DECIMAL
from app.core.database import Base
import enum
from datetime import datetime


class UserRole(str, enum.Enum):
    """用户角色"""
    ADMIN = "admin"           # 管理员
    DISPATCHER = "dispatcher" # 调度员
    DRIVER = "driver"         # 司机
    INSTALLER = "installer"   # 安装师傅
    UNLOADER = "unloader"     # 卸货人员


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(String(32), primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), index=True)
    avatar_url = Column(String(500))
    role = Column(Enum(UserRole), nullable=False, index=True)
    region_id = Column(String(32))
    latitude = Column(DECIMAL(10, 7))
    longitude = Column(DECIMAL(10, 7))
    status = Column(Boolean, default=True)
    device_token = Column(String(500))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
