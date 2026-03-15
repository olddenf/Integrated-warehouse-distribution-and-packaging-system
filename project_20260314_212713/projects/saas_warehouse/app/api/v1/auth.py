from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import LoginRequest, LoginResponse, UserResponse
from app.services.user_service import UserService
from app.core.database import get_db
from app.core.security import create_access_token


router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=LoginResponse)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """用户登录"""
    service = UserService(db)
    user = await service.authenticate(data.username, data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 生成Token
    access_token = create_access_token(
        data={"sub": user.id, "username": user.username, "role": user.role.value}
    )
    
    return LoginResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )
