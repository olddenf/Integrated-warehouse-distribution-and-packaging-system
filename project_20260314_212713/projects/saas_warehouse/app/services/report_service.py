from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, extract
from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.models.order import Order, OrderStatus
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.repositories.order_repository import OrderRepository
from app.utils.id_generator import generate_uuid


class ReportService:
    """报表服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repo = OrderRepository(db)
    
    async def get_order_report(
        self, 
        start_date: str, 
        end_date: str, 
        group_by: str = "day"
    ) -> Dict[str, Any]:
        """订单报表"""
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        
        # 汇总统计
        summary = await self.order_repo.get_statistics(start_dt, end_dt)
        
        # 趋势数据
        trend = await self._get_order_trend(start_dt, end_dt, group_by)
        
        return {
            "summary": summary,
            "trend": trend
        }
    
    async def _get_order_trend(
        self, 
        start_dt: datetime, 
        end_dt: datetime, 
        group_by: str
    ) -> List[Dict[str, Any]]:
        """获取订单趋势"""
        if group_by == "day":
            date_format = func.date(Order.create_time)
        elif group_by == "week":
            date_format = func.concat(
                extract('year', Order.create_time),
                '-W',
                extract('week', Order.create_time)
            )
        else:  # month
            date_format = func.concat(
                extract('year', Order.create_time),
                '-',
                extract('month', Order.create_time)
            )
        
        stmt = self.db.query(
            date_format.label('date'),
            func.count(Order.id).label('count'),
            func.sum(Order.total_amount).label('amount')
        ).where(
            Order.create_time.between(start_dt, end_dt),
            Order.status != OrderStatus.CANCELLED
        ).group_by(
            date_format
        ).order_by(
            date_format
        )
        
        result = await self.db.execute(stmt)
        
        return [
            {
                "date": str(row.date),
                "count": row.count,
                "amount": float(row.amount or 0)
            }
            for row in result.all()
        ]
    
    async def get_worker_report(
        self, 
        start_date: str, 
        end_date: str
    ) -> List[Dict[str, Any]]:
        """人员工作量报表"""
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        
        # 查询每个人员的任务统计
        stmt = self.db.query(
            User.id,
            User.name,
            User.role,
            func.count(Task.id).label('total_tasks'),
            func.sum(func.case(
                (Task.status == TaskStatus.COMPLETED, 1),
                else_=0
            )).label('completed_tasks')
        ).join(
            Task, User.id == Task.assigned_to
        ).where(
            Task.create_time.between(start_dt, end_dt)
        ).group_by(
            User.id
        )
        
        result = await self.db.execute(stmt)
        
        report = []
        for row in result.all():
            total_tasks = row.total_tasks or 0
            completed_tasks = row.completed_tasks or 0
            completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            report.append({
                "worker_id": row.id,
                "worker_name": row.name,
                "role": row.role.value,
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "completion_rate": round(completion_rate, 2)
            })
        
        return report
    
    async def get_fee_report(
        self, 
        start_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        """费用报表"""
        from app.models.fee import Fee, FeeType
        
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        
        # 总费用
        total_stmt = self.db.query(
            func.sum(Fee.amount)
        ).join(
            Order, Fee.order_id == Order.id
        ).where(
            Order.create_time.between(start_dt, end_dt),
            Order.status != OrderStatus.CANCELLED
        )
        total_amount = await self.db.scalar(total_stmt) or 0
        
        # 按费用类型统计
        type_stmt = self.db.query(
            Fee.fee_type,
            func.sum(Fee.amount).label('amount')
        ).join(
            Order, Fee.order_id == Order.id
        ).where(
            Order.create_time.between(start_dt, end_dt),
            Order.status != OrderStatus.CANCELLED
        ).group_by(
            Fee.fee_type
        )
        type_result = await self.db.execute(type_stmt)
        by_type = {row.fee_type.value: float(row.amount) for row in type_result.all()}
        
        return {
            "total_amount": float(total_amount),
            "by_type": by_type
        }
    
    async def create_export_task(
        self, 
        report_type: str, 
        start_date: str, 
        end_date: str
    ) -> str:
        """创建报表导出任务"""
        from app.models.report import ReportExport, ReportType as ExportReportType, ReportStatus
        
        export_record = ReportExport(
            id=generate_uuid(),
            report_type=ExportReportType(report_type),
            start_date=start_date,
            end_date=end_date,
            status=ReportStatus.GENERATING
        )
        
        self.db.add(export_record)
        await self.db.commit()
        
        return export_record.id
