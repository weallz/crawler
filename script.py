import asyncio
from app.storage import AsyncMinioClient
from minio.error import S3Error

async def check_minio():
    client = AsyncMinioClient()
    try:
        # 触发桶存在性检查/创建
        await client.check_and_create_bucket()  # 内部已做存在性检测
        print("Bucket OK")

        # 生成一次预签名 URL 作为探活（对象名可用不存在的也行，不会访问对象）
        url = await client.get_file_url("health-check-placeholder", expires=60)
        print("Presigned URL generated:", url)
        return True
    except S3Error as exc:
        print("MinIO S3Error:", exc)
    except Exception as exc:
        print("MinIO check failed:", exc)
    return False

if __name__ == "__main__":
    asyncio.run(check_minio())