from sqlalchemy import Column, String, Enum, DateTime, DECIMAL, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
from datetime import datetime


class OrderStatus(str, enum.Enum):
    """订单状态"""
    PENDING = "pending"          # 待派单
    ASSIGNED = "assigned"        # 已派单
    DELIVERING = "delivering"    # 配送中
    INSTALLING = "installing"    # 安装中
    COMPLETED = "completed"      # 已完成
    CANCELLED = "cancelled"      # 已取消


class Order(Base):
    """订单表"""
    __tablename__ = "orders"
    
    id = Column(String(32), primary_key=True, index=True)
    order_no = Column(String(32), unique=True, nullable=False, index=True)
    customer_name = Column(String(50), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)
    latitude = Column(DECIMAL(10, 7))
    longitude = Column(DECIMAL(10, 7))
    appointment_time = Column(DateTime, index=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, index=True)
    total_amount = Column(DECIMAL(10, 2), default=0)
    remark = Column(String(500))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关联关系
    products = relationship("OrderProduct", back_populates="order", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="order", cascade="all, delete-orphan")
    fees = relationship("Fee", back_populates="order", cascade="all, delete-orphan")
    logs = relationship("OrderLog", back_populates="order", cascade="all, delete-orphan")
    status_logs = relationship("OrderStatusLog", back_populates="order", cascade="all, delete-orphan")


class OrderProduct(Base):
    """订单商品表"""
    __tablename__ = "order_products"
    
    id = Column(String(32), primary_key=True, index=True)
    order_id = Column(String(32), ForeignKey("orders.id"), nullable=False, index=True)
    product_name = Column(String(100), nullable=False)
    product_code = Column(String(50))
    quantity = Column(DECIMAL(10, 2), default=1)
    unit = Column(String(20))
    
    # 关联关系
    order = relationship("Order", back_populates="products")


class OrderLog(Base):
    """订单操作日志"""
    __tablename__ = "order_logs"
    
    id = Column(String(32), primary_key=True, index=True)
    order_id = Column(String(32), ForeignKey("orders.id"), nullable=False, index=True)
    action = Column(String(50), nullable=False)
    detail = Column(Text)
    extra = Column(Text)
    create_time = Column(DateTime, default=datetime.now)
    
    # 关联关系
    order = relationship("Order", back_populates="logs")


class OrderStatusLog(Base):
    """订单状态变更日志"""
    __tablename__ = "order_status_logs"
    
    id = Column(String(32), primary_key=True, index=True)
    order_id = Column(String(32), ForeignKey("orders.id"), nullable=False, index=True)
    from_status = Column(Enum(OrderStatus), nullable=False)
    to_status = Column(Enum(OrderStatus), nullable=False)
    operator_id = Column(String(32))
    remark = Column(String(500))
    create_time = Column(DateTime, default=datetime.now)
    
    # 关联关系
    order = relationship("Order", back_populates="status_logs")
