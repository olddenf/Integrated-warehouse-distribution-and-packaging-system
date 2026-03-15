from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user_repository import UserRepository
from app.core.security import get_password_hash, verify_password
from app.utils.id_generator import generate_uuid


class UserService:
    """用户服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
    
    async def create_user(self, data: UserCreate) -> User:
        """创建用户"""
        # 检查用户名是否已存在
        existing_user = await self.user_repo.get_by_username(data.username)
        if existing_user:
            raise ValueError("用户名已存在")
        
        # 检查手机号是否已存在
        if data.phone:
            existing_phone = await self.user_repo.get_by_phone(data.phone)
            if existing_phone:
                raise ValueError("手机号已存在")
        
        # 创建用户
        user = User(
            id=generate_uuid(),
            username=data.username,
            password_hash=get_password_hash(data.password),
            name=data.name,
            phone=data.phone,
            role=data.role,
            status=True
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def get_user(self, user_id: str) -> User:
        """获取用户详情"""
        user = await self.user_repo.get(user_id)
        if not user:
            raise ValueError("用户不存在")
        return user
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return await self.user_repo.get_by_username(username)
    
    async def update_user(self, user_id: str, data: UserUpdate) -> User:
        """更新用户"""
        user = await self.get_user(user_id)
        
        # 检查手机号是否已被其他用户使用
        if data.phone and data.phone != user.phone:
            existing_phone = await self.user_repo.get_by_phone(data.phone)
            if existing_phone and existing_phone.id != user_id:
                raise ValueError("手机号已被其他用户使用")
        
        # 更新用户信息
        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def delete_user(self, user_id: str) -> None:
        """删除用户"""
        user = await self.get_user(user_id)
        await self.user_repo.delete(user)
    
    async def authenticate(self, username: str, password: str) -> Optional[User]:
        """用户认证"""
        user = await self.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        if not user.status:
            return None
        return user
    
    async def get_workers_by_role(self, role: UserRole) -> List[User]:
        """获取指定角色的工人"""
        return await self.user_repo.get_active_workers_by_role(role)
