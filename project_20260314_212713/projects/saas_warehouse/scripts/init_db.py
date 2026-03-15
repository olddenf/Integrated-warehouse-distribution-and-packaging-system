import asyncio
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.models import user, order, task, fee, report


async def init_database():
    """初始化数据库表结构"""
    print("开始初始化数据库...")
    
    # 导入所有模型，确保它们被注册到Base.metadata
    # 上面的import语句已经导入了所有模型
    
    async with engine.begin() as conn:
        # 先删除所有表
        await conn.run_sync(Base.metadata.drop_all)
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)
    
    print("数据库初始化完成！")


if __name__ == "__main__":
    asyncio.run(init_database())
