from sqlalchemy import Column, String, Enum, DateTime, DECIMAL, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
from datetime import datetime


class TaskType(str, enum.Enum):
    """任务类型"""
    UNLOAD = "unload"       # 卸货
    DELIVERY = "delivery"   # 配送
    INSTALL = "install"     # 安装


class TaskStatus(str, enum.Enum):
    """任务状态"""
    PENDING = "pending"          # 待处理
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"      # 已完成
    CANCELLED = "cancelled"      # 已取消


class Task(Base):
    """任务表"""
    __tablename__ = "tasks"
    
    id = Column(String(32), primary_key=True, index=True)
    task_no = Column(String(32), unique=True, nullable=False, index=True)
    order_id = Column(String(32), ForeignKey("orders.id"), nullable=False, index=True)
    task_type = Column(Enum(TaskType), nullable=False)
    assigned_to = Column(String(32), ForeignKey("users.id"), index=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    actual_distance = Column(DECIMAL(10, 2))
    remark = Column(Text)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关联关系
    order = relationship("Order", back_populates="tasks")
    assigned_worker = relationship("User")
    records = relationship("TaskRecord", back_populates="task", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="task", cascade="all, delete-orphan")


class TaskRecord(Base):
    """任务执行记录表"""
    __tablename__ = "task_records"
    
    id = Column(String(32), primary_key=True, index=True)
    task_id = Column(String(32), ForeignKey("tasks.id"), nullable=False, index=True)
    record_type = Column(String(50), nullable=False)  # start/complete/photo/location/exception
    content = Column(Text)
    location_lat = Column(DECIMAL(10, 7))
    location_lng = Column(DECIMAL(10, 7))
    create_time = Column(DateTime, default=datetime.now)
    
    # 关联关系
    task = relationship("Task", back_populates="records")


class Attachment(Base):
    """附件表"""
    __tablename__ = "attachments"
    
    id = Column(String(32), primary_key=True, index=True)
    task_id = Column(String(32), ForeignKey("tasks.id"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_size = Column(DECIMAL(10, 2))
    file_type = Column(String(50))
    upload_by = Column(String(32))
    create_time = Column(DateTime, default=datetime.now)
    
    # 关联关系
    task = relationship("Task", back_populates="attachments")


class TaskDispatchLog(Base):
    """任务调度日志"""
    __tablename__ = "task_dispatch_logs"
    
    id = Column(String(32), primary_key=True, index=True)
    task_id = Column(String(32), ForeignKey("tasks.id"), nullable=False, index=True)
    old_worker_id = Column(String(32))
    new_worker_id = Column(String(32))
    operator_id = Column(String(32))
    reason = Column(String(500))
    create_time = Column(DateTime, default=datetime.now)
    
    # 关联关系
    task = relationship("Task")
