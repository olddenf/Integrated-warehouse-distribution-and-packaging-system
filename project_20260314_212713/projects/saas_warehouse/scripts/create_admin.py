import asyncio
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from app.utils.id_generator import generate_uuid


async def create_admin():
    """创建管理员用户"""
    async with AsyncSessionLocal() as session:
        # 检查是否已存在管理员
        from sqlalchemy import select
        result = await session.execute(
            select(User).where(User.role == UserRole.ADMIN)
        )
        existing_admin = result.scalar_one_or_none()
        
        if existing_admin:
            print(f"管理员已存在: {existing_admin.username}")
            return
        
        # 创建管理员用户
        admin = User(
            id=generate_uuid(),
            username="admin",
            password_hash=get_password_hash("admin123"),
            name="系统管理员",
            phone="13800138000",
            role=UserRole.ADMIN,
            status=True
        )
        
        session.add(admin)
        await session.commit()
        print("管理员用户创建成功！")
        print(f"用户名: admin")
        print(f"密码: admin123")


if __name__ == "__main__":
    asyncio.run(create_admin())
