"""
MinIO客户端使用示例
演示如何使用AsyncMinioClient进行文件上传和URL获取
"""
import asyncio
import tempfile
import os

from app.storage import AsyncMinioClient


async def create_sample_image():
    """创建一个示例图片文件用于测试"""
    # 创建临时文件作为示例图片
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    temp_file.write(b"This is a sample image content for testing MinIO upload")
    temp_file.flush()
    temp_file.close()
    return temp_file.name


async def main():
    """主函数，演示MinIO客户端的使用"""
    # 创建MinIO客户端实例
    minio_client = AsyncMinioClient()
    
    try:
        # 检查并创建存储桶
        await minio_client.check_and_create_bucket()
        
        # 创建示例文件
        sample_file_path = await create_sample_image()
        print(f"Created sample file: {sample_file_path}")
        
        # 上传文件
        object_name = await minio_client.upload_file(sample_file_path)
        print(f"File uploaded with object name: {object_name}")
        
        # 获取文件URL
        file_url = await minio_client.get_file_url(object_name)
        print(f"File URL: {file_url}")
        
        # 清理临时文件
        os.unlink(sample_file_path)
        print("Cleaned up temporary file")
        
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # 关闭客户端
        await minio_client.close()


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())