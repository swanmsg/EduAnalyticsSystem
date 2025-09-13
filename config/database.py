"""
数据库配置和初始化
"""
import asyncio
from typing import AsyncGenerator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

# 创建基础模型类
Base = declarative_base()

# 数据库引擎
engine = None
async_engine = None
SessionLocal = None
AsyncSessionLocal = None


def get_database_url() -> str:
    """获取数据库URL"""
    url = settings.DATABASE_URL
    
    # 如果是SQLite，确保目录存在
    if url.startswith("sqlite"):
        import os
        db_path = url.replace("sqlite:///", "")
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)
    
    return url


async def init_db():
    """初始化数据库"""
    global engine, async_engine, SessionLocal, AsyncSessionLocal
    
    try:
        database_url = get_database_url()
        logger.info(f"正在初始化数据库: {database_url}")
        
        # 同步引擎（用于创建表）
        engine = create_engine(database_url, echo=settings.DEBUG)
        
        # 异步引擎
        if database_url.startswith("sqlite"):
            async_database_url = database_url.replace("sqlite:///", "sqlite+aiosqlite:///")
        else:
            async_database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
        
        async_engine = create_async_engine(
            async_database_url,
            echo=settings.DEBUG,
            pool_pre_ping=True
        )
        
        # 会话工厂
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
        
        AsyncSessionLocal = async_sessionmaker(
            bind=async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # 导入所有模型
        from models import student, case, log, score, analysis
        
        # 创建表
        Base.metadata.create_all(bind=engine)
        
        logger.info("✅ 数据库初始化成功")
        
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {str(e)}")
        raise


def get_db() -> SessionLocal:
    """获取同步数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """获取异步数据库会话"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def close_db():
    """关闭数据库连接"""
    global engine, async_engine
    
    if async_engine:
        await async_engine.dispose()
    
    if engine:
        engine.dispose()
    
    logger.info("数据库连接已关闭")