"""
数据库模块使用示例
演示如何使用异步数据库模块进行增删改查操作
"""
import sys
from pathlib import Path
import json
from datetime import datetime as dt

# #region agent log
try:
    with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"db_usage_example.py:11","message":"Python path check","data":{"sys_executable":sys.executable,"sys_path":sys.path[:3]},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
except: pass
# #endregion

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# #region agent log
try:
    with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"db_usage_example.py:18","message":"Project root added to path","data":{"project_root":str(project_root),"sys_path_0":sys.path[0]},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
except: pass
# #endregion

import asyncio
from datetime import datetime
from typing import List

# #region agent log
try:
    with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"db_usage_example.py:28","message":"Before importing app.db","data":{},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
except: pass
# #endregion

try:
    from app.db import (
        get_db_session,
        init_db,
        close_db,
        check_db_connection,
        KeywordCRUD,
        NoteCRUD,
        CommentCRUD,
    )
    # #region agent log
    try:
        with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"db_usage_example.py:35","message":"app.db imported successfully","data":{},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
    except: pass
    # #endregion
except ImportError as e:
    # #region agent log
    try:
        with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"db_usage_example.py:40","message":"Import error caught","data":{"error_type":type(e).__name__,"error_msg":str(e),"error_args":e.args},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
    except: pass
    # #endregion
    print(f"\n❌ 导入错误: {e}")
    print("\n请检查:")
    print("1. 是否安装了所有依赖: pip install -r requirements.txt")
    print("2. 是否在正确的Python环境中运行")
    print("3. 虚拟环境是否已激活（如果使用虚拟环境）")
    raise
except Exception as e:
    # #region agent log
    try:
        with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"C","location":"db_usage_example.py:50","message":"Unexpected import error","data":{"error_type":type(e).__name__,"error_msg":str(e)},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
    except: pass
    # #endregion
    raise


async def example_keyword_operations():
    """关键词操作示例"""
    print("\n" + "="*50)
    print("关键词操作示例")
    print("="*50)
    
    async with get_db_session() as session:
        # 1. 创建关键词
        print("\n1. 创建关键词")
        try:
            keyword1 = await KeywordCRUD.create(
                session=session,
                keyword="Python编程",
                status=1,
                priority=10
            )
            print(f"   创建成功: {keyword1}")
            
            keyword2 = await KeywordCRUD.create(
                session=session,
                keyword="机器学习",
                status=1,
                priority=8
            )
            print(f"   创建成功: {keyword2}")
        except ValueError as e:
            print(f"   关键词已存在: {e}")
        
        # 2. 查询关键词
        print("\n2. 查询关键词")
        keyword = await KeywordCRUD.get_by_keyword(session, "Python编程")
        if keyword:
            print(f"   查询结果: {keyword}")
        
        # 3. 获取待爬取的关键词列表
        print("\n3. 获取待爬取的关键词列表")
        pending_keywords = await KeywordCRUD.get_pending_keywords(session, limit=10)
        print(f"   待爬取关键词数量: {len(pending_keywords)}")
        for kw in pending_keywords:
            print(f"   - {kw.keyword} (优先级: {kw.priority})")
        
        # 4. 更新关键词状态
        print("\n4. 更新关键词状态")
        if keyword:
            updated = await KeywordCRUD.update(
                session=session,
                keyword_id=keyword.id,
                status=2,  # 爬取中
                last_crawl_time=datetime.now()
            )
            print(f"   更新成功: {updated}")
        
        # 5. 获取所有关键词
        print("\n5. 获取所有关键词")
        all_keywords = await KeywordCRUD.get_all(session, limit=10)
        print(f"   关键词总数: {len(all_keywords)}")
        for kw in all_keywords:
            print(f"   - {kw.keyword} (状态: {kw.status}, 笔记数: {kw.total_notes})")


async def example_note_operations():
    """笔记操作示例"""
    print("\n" + "="*50)
    print("笔记操作示例")
    print("="*50)
    
    async with get_db_session() as session:
        # 1. 获取关键词（用于关联）
        keyword = await KeywordCRUD.get_by_keyword(session, "Python编程")
        if not keyword:
            print("   未找到关键词，请先创建关键词")
            return
        
        # 2. 创建单个笔记
        print("\n1. 创建单个笔记")
        try:
            note = await NoteCRUD.create(
                session=session,
                keyword_id=keyword.id,
                note_id="note_123456789",
                title="Python异步编程入门",
                content="这是一篇关于Python异步编程的教程...",
                author_id="author_001",
                author_name="Python开发者",
                author_avatar_url="minio://avatars/author_001.jpg",
                like_count=1024,
                collect_count=256,
                comment_count=128,
                share_count=64,
                view_count=10000,
                cover_image_url="minio://images/cover_001.jpg",
                image_urls=["minio://images/img1.jpg", "minio://images/img2.jpg"],
                note_url="https://www.xiaohongshu.com/explore/123456789",
                publish_time=datetime.now()
            )
            print(f"   创建成功: {note.title}")
        except ValueError as e:
            print(f"   笔记已存在: {e}")
            note = await NoteCRUD.get_by_note_id(session, "note_123456789")
        
        # 3. 批量创建笔记
        print("\n2. 批量创建笔记")
        notes_data = [
            {
                "keyword_id": keyword.id,
                "note_id": f"note_{i}",
                "title": f"Python教程第{i}篇",
                "content": f"这是第{i}篇Python教程的内容...",
                "author_id": f"author_{i % 3}",
                "author_name": f"作者{i % 3}",
                "like_count": 100 * i,
                "collect_count": 20 * i,
                "comment_count": 10 * i,
                "note_url": f"https://www.xiaohongshu.com/explore/{i}",
                "publish_time": datetime.now()
            }
            for i in range(100, 105)  # 创建5条笔记
        ]
        created_notes = await NoteCRUD.batch_create(session, notes_data)
        print(f"   批量创建成功: {len(created_notes)}条")
        
        # 4. 根据关键词ID查询笔记
        print("\n3. 根据关键词ID查询笔记")
        notes = await NoteCRUD.get_by_keyword_id(
            session=session,
            keyword_id=keyword.id,
            limit=10,
            order_by="like_count"
        )
        print(f"   查询到笔记数量: {len(notes)}")
        for n in notes[:3]:  # 只显示前3条
            print(f"   - {n.title} (点赞: {n.like_count}, 收藏: {n.collect_count})")
        
        # 5. 搜索笔记
        print("\n4. 搜索笔记（点赞数>=500）")
        searched_notes = await NoteCRUD.search(
            session=session,
            keyword_id=keyword.id,
            min_like_count=500,
            limit=10
        )
        print(f"   搜索结果数量: {len(searched_notes)}")
        for n in searched_notes:
            print(f"   - {n.title} (点赞: {n.like_count})")
        
        # 6. 更新笔记
        print("\n5. 更新笔记")
        if note:
            updated_note = await NoteCRUD.update(
                session=session,
                note_id=note.id,
                like_count=2048,
                collect_count=512
            )
            print(f"   更新成功: 点赞数={updated_note.like_count}, 收藏数={updated_note.collect_count}")


async def example_comment_operations():
    """评论操作示例"""
    print("\n" + "="*50)
    print("评论操作示例")
    print("="*50)
    
    async with get_db_session() as session:
        # 1. 获取笔记（用于关联）
        note = await NoteCRUD.get_by_note_id(session, "note_123456789")
        if not note:
            print("   未找到笔记，请先创建笔记")
            return
        
        # 2. 创建评论
        print("\n1. 创建评论")
        try:
            comment = await CommentCRUD.create(
                session=session,
                note_id=note.id,
                comment_id="comment_001",
                content="这篇文章写得真好，学到了很多！",
                user_id="user_001",
                user_name="学习爱好者",
                user_avatar_url="minio://avatars/user_001.jpg",
                like_count=10,
                comment_time=datetime.now()
            )
            print(f"   创建成功: {comment.content[:30]}...")
        except ValueError as e:
            print(f"   评论已存在: {e}")
            comment = await CommentCRUD.get_by_comment_id(session, "comment_001")
        
        # 3. 创建回复评论
        print("\n2. 创建回复评论")
        if comment:
            try:
                reply = await CommentCRUD.create(
                    session=session,
                    note_id=note.id,
                    comment_id="comment_002",
                    content="同感！我也觉得很有帮助",
                    user_id="user_002",
                    user_name="另一个用户",
                    parent_comment_id=comment.comment_id,
                    like_count=5,
                    comment_time=datetime.now()
                )
                print(f"   回复创建成功: {reply.content}")
            except ValueError as e:
                print(f"   回复已存在: {e}")
        
        # 4. 批量创建评论
        print("\n3. 批量创建评论")
        comments_data = [
            {
                "note_id": note.id,
                "comment_id": f"comment_{i}",
                "content": f"这是第{i}条评论内容",
                "user_id": f"user_{i}",
                "user_name": f"用户{i}",
                "like_count": i * 2,
                "comment_time": datetime.now()
            }
            for i in range(10, 15)  # 创建5条评论
        ]
        created_comments = await CommentCRUD.batch_create(session, comments_data)
        print(f"   批量创建成功: {len(created_comments)}条")
        
        # 5. 查询笔记的所有评论
        print("\n4. 查询笔记的所有评论")
        comments = await CommentCRUD.get_by_note_id(
            session=session,
            note_id=note.id,
            limit=20,
            order_by="like_count"
        )
        print(f"   评论总数: {len(comments)}")
        for c in comments[:5]:  # 只显示前5条
            print(f"   - {c.user_name}: {c.content[:30]}... (点赞: {c.like_count})")
        
        # 6. 查询评论的回复
        print("\n5. 查询评论的回复")
        if comment:
            replies = await CommentCRUD.get_replies(
                session=session,
                parent_comment_id=comment.comment_id
            )
            print(f"   回复数量: {len(replies)}")
            for r in replies:
                print(f"   - {r.user_name}: {r.content[:30]}...")


async def example_query_by_keyword():
    """按关键词查询爬取结果示例"""
    print("\n" + "="*50)
    print("按关键词查询爬取结果示例")
    print("="*50)
    
    async with get_db_session() as session:
        # 1. 获取关键词
        keyword = await KeywordCRUD.get_by_keyword(session, "Python编程")
        if not keyword:
            print("   未找到关键词")
            return
        
        print(f"\n关键词: {keyword.keyword}")
        print(f"状态: {keyword.status}")
        print(f"已爬取笔记数: {keyword.total_notes}")
        
        # 2. 查询该关键词下的所有笔记
        notes = await NoteCRUD.get_by_keyword_id(
            session=session,
            keyword_id=keyword.id,
            limit=10,
            order_by="like_count"
        )
        
        print(f"\n笔记列表 (共{len(notes)}条):")
        for i, note in enumerate(notes, 1):
            print(f"\n{i}. {note.title}")
            print(f"   作者: {note.author_name}")
            print(f"   点赞: {note.like_count} | 收藏: {note.collect_count} | 评论: {note.comment_count}")
            print(f"   发布时间: {note.publish_time}")
            
            # 查询该笔记的评论
            comments = await CommentCRUD.get_by_note_id(
                session=session,
                note_id=note.id,
                limit=5
            )
            if comments:
                print(f"   评论 ({len(comments)}条):")
                for j, comment in enumerate(comments[:3], 1):  # 只显示前3条
                    print(f"      {j}. {comment.user_name}: {comment.content[:40]}...")


async def main():
    """主函数"""
    # #region agent log
    try:
        with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"G","location":"db_usage_example.py:371","message":"main() function started","data":{},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
    except: pass
    # #endregion
    
    print("="*50)
    print("数据库模块使用示例")
    print("="*50)
    
    # 1. 检查数据库连接
    print("\n1. 检查数据库连接")
    # #region agent log
    try:
        with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"G","location":"db_usage_example.py:382","message":"Before check_db_connection","data":{},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
    except: pass
    # #endregion
    
    is_connected = await check_db_connection()
    
    # #region agent log
    try:
        with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"G","location":"db_usage_example.py:386","message":"After check_db_connection","data":{"is_connected":is_connected},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
    except: pass
    # #endregion
    
    if not is_connected:
        print("   数据库连接失败，请检查配置")
        return
    print("   数据库连接成功")
    
    # 2. 初始化数据库（创建表）
    print("\n2. 初始化数据库")
    # #region agent log
    try:
        with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"G","location":"db_usage_example.py:400","message":"Before init_db","data":{},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
    except: pass
    # #endregion
    
    try:
        await init_db()
        # #region agent log
        try:
            with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"G","location":"db_usage_example.py:405","message":"init_db completed successfully","data":{},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
        except: pass
        # #endregion
        print("   数据库表创建成功")
    except Exception as e:
        # #region agent log
        try:
            with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"G","location":"db_usage_example.py:410","message":"init_db failed","data":{"error_type":type(e).__name__,"error_msg":str(e)},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
        except: pass
        # #endregion
        print(f"   数据库表创建失败: {e}")
        return
    
    # 3. 运行示例
    try:
        await example_keyword_operations()
        await example_note_operations()
        await example_comment_operations()
        await example_query_by_keyword()
    except Exception as e:
        print(f"\n执行示例时出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 4. 关闭数据库连接
        print("\n4. 关闭数据库连接")
        await close_db()
        print("   数据库连接已关闭")


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())

