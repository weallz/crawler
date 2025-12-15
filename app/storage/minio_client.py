"""
异步MinIO存储工具模块
提供图片/视频等文件的异步上传和管理功能
"""
import os
import uuid
from datetime import timedelta
from typing import Optional
from pathlib import Path

from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error
import asyncio
from concurrent.futures import ThreadPoolExecutor

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()


class AsyncMinioClient:
    """
    异步MinIO客户端
    提供文件上传、下载、删除等操作的异步接口
    """

    def __init__(self):
        """初始化MinIO客户端"""
        # 从环境变量读取配置
        self.endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        self.access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
        self.secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
        self.bucket_name = os.getenv("MINIO_BUCKET_NAME", "xiaohongshu-storage")
        self.secure = os.getenv("MINIO_SECURE", "false").lower() == "true"
        
        # 创建MinIO客户端实例
        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )
        
        # 创建线程池用于异步操作
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        logger.info(f"MinIO client initialized: endpoint={self.endpoint}, bucket={self.bucket_name}")

    async def _run_in_executor(self, func, *args, **kwargs):
        """
        在线程池中运行同步函数
        
        Args:
            func: 要执行的函数
            *args: 函数的位置参数
            **kwargs: 函数的关键字参数
            
        Returns:
            函数执行结果
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, lambda: func(*args, **kwargs))

    async def check_and_create_bucket(self) -> bool:
        """
        检查存储桶是否存在，不存在则创建
        
        Returns:
            bool: 存储桶是否存在或创建成功返回True，否则返回False
            
        Raises:
            S3Error: MinIO服务相关异常
        """
        try:
            exists = await self._run_in_executor(
                self.client.bucket_exists, 
                self.bucket_name
            )
            
            if not exists:
                logger.info(f"Bucket {self.bucket_name} does not exist, creating...")
                await self._run_in_executor(
                    self.client.make_bucket, 
                    self.bucket_name
                )
                logger.info(f"Bucket {self.bucket_name} created successfully")
            
            logger.info(f"Bucket {self.bucket_name} is ready")
            return True
            
        except S3Error as e:
            logger.error(f"Failed to check or create bucket {self.bucket_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error when checking or creating bucket: {e}")
            raise

    async def upload_file(self, file_path: str, object_name: Optional[str] = None) -> str:
        """
        异步上传文件到MinIO
        
        Args:
            file_path (str): 本地文件路径
            object_name (Optional[str]): 对象名称，如果不指定则自动生成UUID
            
        Returns:
            str: 上传后的对象名称
            
        Raises:
            FileNotFoundError: 本地文件不存在
            S3Error: MinIO服务相关异常
        """
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # 生成唯一的对象名称
        if object_name is None:
            file_extension = Path(file_path).suffix
            object_name = f"{uuid.uuid4().hex}{file_extension}"
            
        try:
            # 获取文件大小
            file_stat = os.stat(file_path)
            
            # 异步上传文件
            await self._run_in_executor(
                self.client.fput_object,
                self.bucket_name,
                object_name,
                file_path,
                metadata={'Content-Type': 'application/octet-stream'}
            )
            
            logger.info(f"File uploaded successfully: {file_path} -> {object_name}")
            return object_name
            
        except S3Error as e:
            logger.error(f"Failed to upload file {file_path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error when uploading file {file_path}: {e}")
            raise

    async def get_file_url(self, object_name: str, expires: int = 7*24*60*60) -> str:
        """
        获取文件的预签名URL
        
        Args:
            object_name (str): 对象名称
            expires (int): URL过期时间（秒），默认7天
            
        Returns:
            str: 文件访问URL
            
        Raises:
            S3Error: MinIO服务相关异常
        """
        try:
            url = await self._run_in_executor(
                self.client.presigned_get_object,
                self.bucket_name,
                object_name,
                timedelta(seconds=expires)
            )
            
            logger.debug(f"Generated presigned URL for {object_name}")
            return url
            
        except S3Error as e:
            logger.error(f"Failed to generate presigned URL for {object_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error when generating presigned URL: {e}")
            raise

    async def close(self):
        """关闭客户端，释放资源"""
        self.executor.shutdown(wait=True)
        logger.info("MinIO client closed")
