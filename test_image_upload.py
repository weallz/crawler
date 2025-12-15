#!/usr/bin/env python3
"""
图片上传功能测试脚本
用于验证MinIO图片上传功能及生成的URL是否可以在浏览器中访问
"""

import asyncio
import tempfile
import os
import requests
from app.storage import AsyncMinioClient


async def test_image_upload_and_url_access():
    """测试图片上传和URL访问功能"""
    print("开始测试图片上传功能...")
    
    # 创建MinIO客户端
    client = AsyncMinioClient()
    
    try:
        # 检查并创建存储桶
        print("检查存储桶...")
        await client.check_and_create_bucket()
        print("✓ 存储桶检查完成")
        
        # 创建测试图片文件
        print("创建测试图片文件...")
        test_image_content = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
            b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe\x02\xfe'
            b'\xdc\xccY\xe7\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp.write(test_image_content)
            tmp.flush()
            test_file_path = tmp.name
        
        print(f"✓ 测试图片创建完成: {test_file_path}")
        
        # 上传图片
        print("上传图片...")
        object_name = await client.upload_file(test_file_path, "test-image.png")
        print(f"✓ 图片上传成功，对象名: {object_name}")
        
        # 获取访问URL
        print("生成访问URL...")
        file_url = await client.get_file_url(object_name, expires=3600)  # 1小时过期
        print(f"✓ URL生成成功: {file_url}")
        
        # 测试URL可访问性
        print("测试URL可访问性...")
        try:
            response = requests.get(file_url, timeout=10)
            if response.status_code == 200:
                print("✓ URL可正常访问")
                print(f"\n请在浏览器中打开以下URL进行验证:")
                print(file_url)
            else:
                print(f"✗ URL访问失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"✗ URL访问出错: {e}")
        
        # 清理测试文件
        os.unlink(test_file_path)
        print("✓ 本地测试文件清理完成")
        
        return object_name, file_url
        
    except Exception as e:
        print(f"✗ 测试过程中发生错误: {e}")
        raise
    finally:
        await client.close()


async def list_bucket_contents():
    """列出存储桶中的所有对象"""
    print("\n检查存储桶内容...")
    client = AsyncMinioClient()
    
    try:
        # 列出存储桶中的对象
        objects = client.client.list_objects(client.bucket_name)
        print(f"存储桶 '{client.bucket_name}' 中的对象:")
        
        object_count = 0
        for obj in objects:
            print(f"  - {obj.object_name} ({obj.size} bytes, {obj.last_modified})")
            object_count += 1
            
        if object_count == 0:
            print("  存储桶为空")
        else:
            print(f"总共 {object_count} 个对象")
            
    except Exception as e:
        print(f"✗ 列出存储桶内容时出错: {e}")
    finally:
        await client.close()


if __name__ == "__main__":
    print("=" * 50)
    print("小红书爬虫项目 - 图片上传功能测试")
    print("=" * 50)
    
    # 运行上传测试
    asyncio.run(test_image_upload_and_url_access())
    
    # 显示存储桶内容
    asyncio.run(list_bucket_contents())
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)