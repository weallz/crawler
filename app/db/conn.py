"""
数据库连接模块
提供异步MySQL数据库连接和会话管理
"""
import os
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from dotenv import load_dotenv
# #region agent log
import json
from datetime import datetime as dt
try:
    with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"D","location":"conn.py:19","message":"Before importing loguru","data":{},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
except: pass
# #endregion
try:
    from loguru import logger
    # #region agent log
    try:
        with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"D","location":"conn.py:25","message":"loguru imported successfully","data":{},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
    except: pass
    # #endregion
except ImportError as e:
    # #region agent log
    try:
        with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"D","location":"conn.py:30","message":"loguru import failed","data":{"error_type":type(e).__name__,"error_msg":str(e)},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
    except: pass
    # #endregion
    raise

# 加载环境变量
load_dotenv()

# 创建ORM基类
Base = declarative_base()

# 全局变量
_engine: AsyncEngine | None = None
_async_session_maker: async_sessionmaker[AsyncSession] | None = None


def get_database_url() -> str:
    """
    从环境变量构建数据库连接URL
    
    Returns:
        str: 数据库连接URL
        
    Raises:
        ValueError: 当必需的环境变量缺失时
    """
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = int(os.getenv("DB_PORT", "3306"))
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "xiaohongshu_spider")
    db_charset = os.getenv("DB_CHARSET", "utf8mb4")
    
    if not db_user:
        raise ValueError("DB_USER environment variable is required")
    if not db_name:
        raise ValueError("DB_NAME environment variable is required")
    
    # SQLAlchemy 2.0+ 异步MySQL连接URL格式
    # 使用 aiomysql 驱动
    database_url = (
        f"mysql+aiomysql://{db_user}:{db_password}@{db_host}:{db_port}/"
        f"{db_name}?charset={db_charset}"
    )
    
    return database_url


def create_engine() -> AsyncEngine:
    """
    创建异步数据库引擎
    
    Returns:
        AsyncEngine: SQLAlchemy异步引擎实例
    """
    database_url = get_database_url()
    
    # 获取数据库配置信息（用于日志）
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "xiaohongshu_spider")
    
    # 连接池配置
    pool_size = int(os.getenv("DB_POOL_SIZE", "10"))
    max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", "30"))
    pool_recycle = int(os.getenv("DB_POOL_RECYCLE", "3600"))
    echo = os.getenv("DB_ECHO", "False").lower() == "true"
    
    # #region agent log
    try:
        with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                "sessionId": "debug-session",
                "runId": "pre-fix",
                "hypothesisId": "H1",
                "location": "conn.py:108",
                "message": "create_async_engine parameters",
                "data": {
                    "pool_size": pool_size,
                    "max_overflow": max_overflow,
                    "pool_timeout": pool_timeout,
                    "pool_recycle": pool_recycle,
                    "echo": echo,
                    "db_url_scheme": database_url.split(':', 1)[0] if database_url else None
                },
                "timestamp": int(dt.now().timestamp() * 1000)
            }) + '\n')
    except:
        pass
    # #endregion

    engine = create_async_engine(
        database_url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
        pool_recycle=pool_recycle,
        echo=echo,  # 是否打印SQL语句（开发环境可开启）
        future=True,
        # aiomysql特定参数
        connect_args={
            "charset": "utf8mb4",
            "autocommit": False,
        }
    )
    
    logger.info(
        f"Database engine created: {db_host}:{db_port}/{db_name} "
        f"(pool_size={pool_size}, max_overflow={max_overflow})"
    )
    
    return engine


def get_engine() -> AsyncEngine:
    """
    获取数据库引擎（单例模式）
    
    Returns:
        AsyncEngine: 数据库引擎实例
    """
    global _engine
    if _engine is None:
        _engine = create_engine()
    return _engine


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    """
    获取异步会话工厂（单例模式）
    
    Returns:
        async_sessionmaker: 异步会话工厂
    """
    global _async_session_maker
    if _async_session_maker is None:
        engine = get_engine()
        # #region agent log
        try:
            with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    "sessionId": "debug-session",
                    "runId": "pre-fix",
                    "hypothesisId": "H2",
                    "location": "conn.py:175",
                    "message": "sessionmaker using engine",
                    "data": {
                        "engine_cls": type(engine).__name__,
                        "dialect": getattr(engine, "dialect", None).__class__.__name__ if getattr(engine, "dialect", None) else None
                    },
                    "timestamp": int(dt.now().timestamp() * 1000)
                }) + '\n')
        except:
            pass
        # #endregion
        _async_session_maker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
    return _async_session_maker


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    获取异步数据库会话（依赖注入使用）
    
    Yields:
        AsyncSession: 异步数据库会话
        
    Example:
        async with get_session() as session:
            result = await session.execute(select(User))
    """
    async_session_maker = get_session_maker()
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话的上下文管理器
    
    Yields:
        AsyncSession: 异步数据库会话
        
    Example:
        async with get_db_session() as session:
            result = await session.execute(select(User))
    """
    async_session_maker = get_session_maker()
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database transaction error: {e}")
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    初始化数据库（创建所有表）
    
    Note:
        生产环境建议使用Alembic进行数据库迁移
    """
    try:
        engine = get_engine()
        async with engine.begin() as conn:
            # 导入所有模型以确保它们被注册到Base.metadata
            from app.db import models  # noqa: F401
            
            # 创建所有表
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def close_db() -> None:
    """
    关闭数据库连接池
    """
    global _engine, _async_session_maker
    if _engine:
        await _engine.dispose()
        _engine = None
        _async_session_maker = None
        logger.info("Database connections closed")


async def check_db_connection() -> bool:
    """
    检查数据库连接是否正常
    
    Returns:
        bool: 连接是否正常
    """
    try:
        # #region agent log
        try:
            try:
                import greenlet  # type: ignore
                gl_status = "present"
            except Exception as imp_err:
                gl_status = f"missing:{type(imp_err).__name__}"
            with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    "sessionId": "debug-session",
                    "runId": "pre-fix",
                    "hypothesisId": "H1",
                    "location": "conn.py:272",
                    "message": "greenlet availability before query",
                    "data": {"status": gl_status},
                    "timestamp": int(dt.now().timestamp() * 1000)
                }) + '\n')
        except:
            pass
        # #endregion
        async_session_maker = get_session_maker()
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
        logger.info("Database connection check passed")
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        # #region agent log
        try:
            with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    "sessionId": "debug-session",
                    "runId": "pre-fix",
                    "hypothesisId": "H3",
                    "location": "conn.py:290",
                    "message": "check_db_connection failed",
                    "data": {"error_type": type(e).__name__, "error_msg": str(e)},
                    "timestamp": int(dt.now().timestamp() * 1000)
                }) + '\n')
        except:
            pass
        # #endregion
        return False

