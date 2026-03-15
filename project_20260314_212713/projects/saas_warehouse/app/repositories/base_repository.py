from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Dict, Any, Optional, Type, TypeVar, Generic
from app.core.database import Base

ModelType = TypeVar('ModelType', bound=Base)


class BaseRepository(Generic[ModelType]):
    """基础数据访问层"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model: Type[ModelType] = self.__orig_bases__[0].__args__[0]
    
    async def get(self, id: str) -> Optional[ModelType]:
        """根据ID获取对象"""
        return await self.session.get(self.model, id)
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """获取所有对象"""
        query = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def create(self, **kwargs) -> ModelType:
        """创建对象"""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
    
    async def update(self, instance: ModelType, **kwargs) -> ModelType:
        """更新对象"""
        for field, value in kwargs.items():
            setattr(instance, field, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
    
    async def delete(self, instance: ModelType) -> None:
        """删除对象"""
        await self.session.delete(instance)
        await self.session.commit()
    
    async def count(self, **filters) -> int:
        """统计数量"""
        query = select(func.count(self.model.id))
        for field, value in filters.items():
            if field.endswith('__ilike'):
                field_name = field.split('__')[0]
                query = query.where(getattr(self.model, field_name).ilike(value))
            elif field.endswith('__gte'):
                field_name = field.split('__')[0]
                query = query.where(getattr(self.model, field_name) >= value)
            elif field.endswith('__lte'):
                field_name = field.split('__')[0]
                query = query.where(getattr(self.model, field_name) <= value)
            else:
                query = query.where(getattr(self.model, field) == value)
        result = await self.session.execute(query)
        return result.scalar() or 0
    
    async def paginate(
        self, 
        filters: Dict[str, Any] = None, 
        order_by: List = None, 
        page: int = 1, 
        size: int = 20
    ) -> Dict[str, Any]:
        """分页查询"""
        query = select(self.model)
        
        # 应用过滤条件
        if filters:
            for field, value in filters.items():
                if value is None:
                    continue
                if field.endswith('__ilike'):
                    field_name = field.split('__')[0]
                    query = query.where(getattr(self.model, field_name).ilike(value))
                elif field.endswith('__gte'):
                    field_name = field.split('__')[0]
                    query = query.where(getattr(self.model, field_name) >= value)
                elif field.endswith('__lte'):
                    field_name = field.split('__')[0]
                    query = query.where(getattr(self.model, field_name) <= value)
                else:
                    query = query.where(getattr(self.model, field) == value)
        
        # 应用排序
        if order_by:
            for order in order_by:
                query = query.order_by(order)
        
        # 计算总数
        total = await self.count(**filters)
        
        # 应用分页
        offset = (page - 1) * size
        query = query.offset(offset).limit(size)
        
        # 执行查询
        result = await self.session.execute(query)
        items = result.scalars().all()
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'size': size
        }
