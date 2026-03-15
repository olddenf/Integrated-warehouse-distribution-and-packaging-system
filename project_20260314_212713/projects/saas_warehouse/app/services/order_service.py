from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.order import Order, OrderStatus, OrderProduct, OrderLog
from app.schemas.order import OrderCreate, OrderUpdate
from app.repositories.order_repository import OrderRepository
from app.utils.id_generator import generate_uuid, generate_order_no
from app.utils.map_client import MapClient
from app.services.fee_service import FeeService
from app.core.state_machine import OrderStateMachine


class OrderService:
    """订单服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.map_client = MapClient()
        self.fee_service = FeeService(db)
    
    async def create_order(self, data: OrderCreate) -> Order:
        """创建订单"""
        # 生成订单编号
        order_no = generate_order_no()
        
        # 地址解析获取经纬度
        try:
            lat, lng = await self.map_client.geocode(data.address)
        except Exception as e:
            lat, lng = None, None
        
        # 创建订单
        order = Order(
            id=generate_uuid(),
            order_no=order_no,
            customer_name=data.customer_name,
            customer_phone=data.customer_phone,
            address=data.address,
            latitude=lat,
            longitude=lng,
            appointment_time=data.appointment_time,
            status=OrderStatus.PENDING,
            total_amount=0,
            remark=data.remark
        )
        
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        
        # 创建商品明细
        for product in data.products:
            order_product = OrderProduct(
                id=generate_uuid(),
                order_id=order.id,
                product_name=product.product_name,
                product_code=product.product_code,
                quantity=product.quantity,
                unit=product.unit
            )
            self.db.add(order_product)
        
        await self.db.commit()
        
        # 自动计算费用
        await self.fee_service.calculate_fees(order.id)
        
        # 记录创建日志
        await self._log_order_action(
            order.id, 
            'CREATE', 
            '创建订单',
            None
        )
        
        # 刷新订单获取总金额
        await self.db.refresh(order)
        
        return order
    
    async def update_order(self, order_id: str, data: OrderUpdate) -> Order:
        """更新订单"""
        order = await self.get_order(order_id)
        
        # 状态校验
        if order.status != OrderStatus.PENDING:
            allowed_fields = {'remark'}
            actual_fields = set(data.dict(exclude_unset=True).keys())
            if not actual_fields.issubset(allowed_fields):
                raise ValueError(f"当前状态{order.status.value}仅允许修改备注")
        
        # 更新字段
        update_data = data.dict(exclude_unset=True)
        
        # 如果地址变化，重新解析
        if 'address' in update_data and update_data['address'] != order.address:
            try:
                lat, lng = await self.map_client.geocode(update_data['address'])
                update_data['latitude'] = lat
                update_data['longitude'] = lng
            except Exception:
                pass
        
        for field, value in update_data.items():
            setattr(order, field, value)
        
        order.update_time = datetime.now()
        await self.db.commit()
        await self.db.refresh(order)
        
        await self._log_order_action(order_id, 'UPDATE', '更新订单', update_data)
        
        return order
    
    async def cancel_order(self, order_id: str, reason: str, operator_id: str) -> Order:
        """取消订单"""
        order = await self.get_order(order_id)
        
        # 状态校验
        if order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
            raise ValueError(f"订单状态{order.status.value}不允许取消")
        
        # 检查进行中的任务
        in_progress_tasks = await self.order_repo.get_in_progress_tasks(order_id)
        if in_progress_tasks:
            raise ValueError("存在进行中的任务，无法取消")
        
        # 取消未开始的任务
        pending_tasks = await self.order_repo.get_pending_tasks(order_id)
        for task in pending_tasks:
            task.status = 'cancelled'
            task.remark = f"订单取消: {reason}"
        
        # 更新订单状态
        old_status = order.status
        order.status = OrderStatus.CANCELLED
        order.update_time = datetime.now()
        
        # 记录状态变更日志
        log = OrderStateMachine.transition(
            order, 
            OrderStatus.CANCELLED, 
            operator_id, 
            f"取消原因: {reason}"
        )
        self.db.add(log)
        
        await self.db.commit()
        
        # 记录操作日志
        await self._log_order_action(
            order_id,
            'CANCEL',
            f'取消订单: {reason}',
            {'old_status': old_status.value, 'new_status': order.status.value}
        )
        
        return order
    
    async def get_order(self, order_id: str) -> Order:
        """获取订单详情"""
        order = await self.order_repo.get(order_id)
        if not order:
            raise ValueError("订单不存在")
        return order
    
    async def get_orders(
        self, 
        status: Optional[str] = None, 
        customer_name: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        page: int = 1,
        size: int = 20
    ) -> Dict[str, Any]:
        """查询订单列表"""
        filters = {}
        if status:
            filters['status'] = status
        if customer_name:
            filters['customer_name__ilike'] = f"%{customer_name}%"
        if start_date:
            filters['create_time__gte'] = start_date
        if end_date:
            filters['create_time__lte'] = end_date
        
        return await self.order_repo.paginate(
            filters=filters,
            order_by=[Order.create_time.desc()],
            page=page,
            size=size
        )
    
    async def _log_order_action(self, order_id: str, action: str, detail: str, extra: Dict[str, Any]):
        """记录订单操作日志"""
        import json
        log = OrderLog(
            id=generate_uuid(),
            order_id=order_id,
            action=action,
            detail=detail,
            extra=json.dumps(extra) if extra else None
        )
        self.db.add(log)
        await self.db.commit()
