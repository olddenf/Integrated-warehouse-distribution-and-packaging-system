from sqlalchemy import Column, String, Enum, DateTime, DECIMAL, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
from datetime import datetime


class FeeType(str, enum.Enum):
    """费用类型"""
    DELIVERY = "delivery"   # 配送费
    INSTALL = "install"     # 安装费
    UNLOAD = "unload"       # 卸货费
    OTHER = "other"         # 其他费用


class FeeStatus(str, enum.Enum):
    """费用状态"""
    CALCULATED = "calculated"  # 已计算
    ADJUSTED = "adjusted"      # 已调整
    CONFIRMED = "confirmed"    # 已确认


class Fee(Base):
    """费用表"""
    __tablename__ = "fees"
    
    id = Column(String(32), primary_key=True, index=True)
    order_id = Column(String(32), ForeignKey("orders.id"), nullable=False, index=True)
    fee_type = Column(Enum(FeeType), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    description = Column(String(255))
    status = Column(Enum(FeeStatus), default=FeeStatus.CALCULATED)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关联关系
    order = relationship("Order", back_populates="fees")
    adjust_logs = relationship("FeeAdjustLog", back_populates="fee", cascade="all, delete-orphan")


class FeeAdjustLog(Base):
    """费用调整日志"""
    __tablename__ = "fee_adjust_logs"
    
    id = Column(String(32), primary_key=True, index=True)
    fee_id = Column(String(32), ForeignKey("fees.id"), nullable=False, index=True)
    old_amount = Column(DECIMAL(10, 2), nullable=False)
    new_amount = Column(DECIMAL(10, 2), nullable=False)
    reason = Column(String(500))
    operator_id = Column(String(32))
    create_time = Column(DateTime, default=datetime.now)
    
    # 关联关系
    fee = relationship("Fee", back_populates="adjust_logs")
