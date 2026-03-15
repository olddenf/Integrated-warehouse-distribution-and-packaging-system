from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """配置管理"""
    
    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./saas_warehouse.db"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT配置
    JWT_SECRET_KEY: str = "saas-warehouse-secret-key-2026"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 120
    
    # 高德地图配置
    AMAP_API_KEY: str = "test-amap-api-key"
    
    # 阿里云OSS配置
    OSS_ACCESS_KEY_ID: str = "test-access-key-id"
    OSS_ACCESS_KEY_SECRET: str = "test-access-key-secret"
    OSS_BUCKET_NAME: str = "test-bucket-name"
    OSS_ENDPOINT: str = "https://oss-cn-beijing.aliyuncs.com"
    
    # Celery配置
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # 加密密钥
    ENCRYPTION_KEY: str = "saas-warehouse-encryption-key-2026"
    
    # 日志级别
    LOG_LEVEL: str = "INFO"
    
    # 项目信息
    PROJECT_NAME: str = "SaaS仓配装一体化管理系统"
    VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()