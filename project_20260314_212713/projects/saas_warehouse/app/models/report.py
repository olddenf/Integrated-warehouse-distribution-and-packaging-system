from sqlalchemy import Column, String, Enum, DateTime, Text
from app.core.database import Base
import enum
from datetime import datetime


class ReportType(str, enum.Enum):
    """报表类型"""
    ORDER = "order"       # 订单报表
    WORKER = "worker"     # 人员报表
    FEE = "fee"           # 费用报表


class ReportStatus(str, enum.Enum):
    """报表状态"""
    GENERATING = "generating"  # 生成中
    COMPLETED = "completed"    # 已完成
    FAILED = "failed"          # 失败


class ReportExport(Base):
    """报表导出记录"""
    __tablename__ = "report_exports"
    
    id = Column(String(32), primary_key=True, index=True)
    report_type = Column(Enum(ReportType), nullable=False)
    start_date = Column(String(20), nullable=False)
    end_date = Column(String(20), nullable=False)
    file_url = Column(String(500))
    status = Column(Enum(ReportStatus), default=ReportStatus.GENERATING)
    error_message = Column(Text)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
