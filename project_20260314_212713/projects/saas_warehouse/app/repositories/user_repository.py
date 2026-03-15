from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.user import User, UserRole
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """用户数据访问层"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = User
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_phone(self, phone: str) -> Optional[User]:
        """根据手机号获取用户"""
        query = select(User).where(User.phone == phone)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_active_workers_by_role(self, role: UserRole) -> List[User]:
        """获取指定角色的活跃用户"""
        query = select(User).where(
            User.role == role,
            User.status == True
        )
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_avg_rating(self, user_id: str) -> float:
        """获取用户平均评价
        这里简化处理，实际应该关联评价表
        """
        # 简化实现，返回默认值
        return 4.5
    
    async def get_worker_skills(self, user_id: str) -> List[str]:
        """获取工人技能
        这里简化处理，实际应该关联技能表
        """
        # 简化实现，返回默认技能
        return ["AC-001", "FURN-001"]
