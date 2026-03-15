from app.models.order import OrderStatus


class OrderStateMachine:
    """
    订单状态机
    
    状态流转规则：
    - PENDING -> ASSIGNED (派单)
    - PENDING -> CANCELLED (取消)
    - ASSIGNED -> DELIVERING (配送中)
    - ASSIGNED -> CANCELLED (取消)
    - DELIVERING -> INSTALLING (安装中)
    - DELIVERING -> CANCELLED (取消)
    - INSTALLING -> COMPLETED (完成)
    """
    
    TRANSITIONS = {
        OrderStatus.PENDING: [OrderStatus.ASSIGNED, OrderStatus.CANCELLED],
        OrderStatus.ASSIGNED: [OrderStatus.DELIVERING, OrderStatus.CANCELLED],
        OrderStatus.DELIVERING: [OrderStatus.INSTALLING, OrderStatus.CANCELLED],
        OrderStatus.INSTALLING: [OrderStatus.COMPLETED],
        OrderStatus.COMPLETED: [],
        OrderStatus.CANCELLED: []
    }
    
    @classmethod
    def can_transition(cls, from_status: OrderStatus, to_status: OrderStatus) -> bool:
        """检查状态是否可以流转"""
        return to_status in cls.TRANSITIONS.get(from_status, [])
    
    @classmethod
    def transition(cls, order, to_status: OrderStatus, operator_id: str, remark: str = None):
        """执行状态流转"""
        from app.models.order import OrderStatusLog
        from datetime import datetime
        
        if not cls.can_transition(order.status, to_status):
            raise ValueError(f"无法从{order.status.value}流转到{to_status.value}")
        
        old_status = order.status
        order.status = to_status
        order.update_time = datetime.now()
        
        # 记录状态变更日志
        log = OrderStatusLog(
            order_id=order.id,
            from_status=old_status,
            to_status=to_status,
            operator_id=operator_id,
            remark=remark,
            create_time=datetime.now()
        )
        
        return log