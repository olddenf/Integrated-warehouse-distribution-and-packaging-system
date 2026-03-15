from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from decimal import Decimal
from app.models.fee import Fee, FeeType, FeeStatus, FeeAdjustLog
from app.models.order import Order
from app.repositories.order_repository import OrderRepository
from app.utils.id_generator import generate_uuid


class FeeService:
    """费用服务"""
    
    # 费率配置
    RATE_CONFIG = {
        "delivery": {
            "base_fee": Decimal("20.00"),
            "per_km_rate": Decimal("5.00"),
        },
        "install": {
            "rates": {
                "AC-001": Decimal("150.00"),
                "FURN-001": Decimal("200.00"),
                "DEFAULT": Decimal("100.00")
            }
        },
        "unload": {
            "per_item_rate": Decimal("5.00")
        }
    }
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.order_repo = OrderRepository(db)
    
    async def calculate_fees(self, order_id: str) -> List[Fee]:
        """计算订单费用"""
        order = await self.order_repo.get(order_id)
        
        fees = []
        
        # 1. 配送费
        delivery_fee = await self._calculate_delivery_fee(order)
        fees.append(Fee(
            id=generate_uuid(),
            order_id=order_id,
            fee_type=FeeType.DELIVERY,
            amount=delivery_fee,
            description="配送费",
            status=FeeStatus.CALCULATED
        ))
        
        # 2. 安装费
        install_fee = await self._calculate_install_fee(order)
        fees.append(Fee(
            id=generate_uuid(),
            order_id=order_id,
            fee_type=FeeType.INSTALL,
            amount=install_fee,
            description="安装费",
            status=FeeStatus.CALCULATED
        ))
        
        # 3. 卸货费
        unload_fee = await self._calculate_unload_fee(order)
        fees.append(Fee(
            id=generate_uuid(),
            order_id=order_id,
            fee_type=FeeType.UNLOAD,
            amount=unload_fee,
            description="卸货费",
            status=FeeStatus.CALCULATED
        ))
        
        # 批量保存
        for fee in fees:
            self.db.add(fee)
        
        # 更新订单总金额
        total_amount = sum(f.amount for f in fees)
        order.total_amount = total_amount
        
        await self.db.commit()
        
        return fees
    
    async def _calculate_delivery_fee(self, order: Order) -> Decimal:
        """计算配送费"""
        config = self.RATE_CONFIG["delivery"]
        
        # 简化实现，使用默认距离10公里
        distance = 10.0
        
        # 计算：基础费 + 距离 * 单价
        fee = config["base_fee"] + Decimal(str(distance)) * config["per_km_rate"]
        
        return fee.quantize(Decimal("0.01"))
    
    async def _calculate_install_fee(self, order: Order) -> Decimal:
        """计算安装费"""
        config = self.RATE_CONFIG["install"]
        total = Decimal("0")
        
        for product in order.products:
            # 获取商品安装费率
            rate = config["rates"].get(
                product.product_code,
                config["rates"]["DEFAULT"]
            )
            
            # 计算
            fee = Decimal(str(product.quantity)) * rate
            total += fee
        
        return total.quantize(Decimal("0.01"))
    
    async def _calculate_unload_fee(self, order: Order) -> Decimal:
        """计算卸货费"""
        config = self.RATE_CONFIG["unload"]
        
        # 计算总数量
        total_quantity = sum(p.quantity for p in order.products)
        
        fee = Decimal(str(total_quantity)) * config["per_item_rate"]
        
        return fee.quantize(Decimal("0.01"))
    
    async def adjust_fee(
        self, 
        fee_id: str, 
        new_amount: Decimal, 
        reason: str, 
        operator_id: str
    ) -> Fee:
        """调整费用"""
        fee = await self.db.get(Fee, fee_id)
        if not fee:
            raise ValueError("费用记录不存在")
        
        old_amount = fee.amount
        fee.amount = new_amount
        fee.status = FeeStatus.ADJUSTED
        fee.description = f"{fee.description} (调整: {reason})"
        
        # 记录调整日志
        log = FeeAdjustLog(
            id=generate_uuid(),
            fee_id=fee_id,
            old_amount=old_amount,
            new_amount=new_amount,
            reason=reason,
            operator_id=operator_id
        )
        self.db.add(log)
        
        # 更新订单总金额
        order = fee.order
        fees = await self.db.execute(
            self.db.query(Fee).where(Fee.order_id == order.id)
        ).scalars().all()
        order.total_amount = sum(f.amount for f in fees)
        
        await self.db.commit()
        await self.db.refresh(fee)
        
        return fee
    
    async def get_fees_by_order(self, order_id: str) -> List[Fee]:
        """获取订单的费用列表"""
        fees = await self.db.execute(
            self.db.query(Fee).where(Fee.order_id == order_id)
        ).scalars().all()
        return fees
