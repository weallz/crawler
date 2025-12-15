# 数据库模块使用说明

## 概述

本项目使用 SQLAlchemy 2.0+ 异步版本 + aiomysql 实现异步数据库操作，适配 Python 3.13.2 和 MySQL 8.1+。

## 目录结构

```
app/db/
├── __init__.py      # 模块导出
├── conn.py          # 数据库连接管理
├── models.py        # 数据模型定义
└── crud.py          # CRUD操作实现
```

## 环境配置

### 1. 创建 .env 文件

在项目根目录创建 `.env` 文件，参考 `env.example`：

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=123456
DB_NAME=xiaohongshu_spider
DB_CHARSET=utf8mb4

# 连接池配置
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
DB_ECHO=false
```

### 2. 创建数据库和表

执行建表SQL：

```bash
mysql -u root -p < db/schema.sql
```

或使用Python初始化：

```python
from app.db import init_db
import asyncio

asyncio.run(init_db())
```

## 快速开始

### 1. 检查数据库连接

```python
from app.db import check_db_connection
import asyncio

async def main():
    is_ok = await check_db_connection()
    print(f"连接状态: {is_ok}")

asyncio.run(main())
```

### 2. 使用数据库会话

```python
from app.db import get_db_session
from app.db.crud import KeywordCRUD

async def main():
    async with get_db_session() as session:
        # 创建关键词
        keyword = await KeywordCRUD.create(
            session=session,
            keyword="Python编程",
            status=1,
            priority=10
        )
        print(f"创建成功: {keyword}")

asyncio.run(main())
```

## CRUD操作示例

### 关键词操作

#### 创建关键词

```python
from app.db import get_db_session, KeywordCRUD

async with get_db_session() as session:
    keyword = await KeywordCRUD.create(
        session=session,
        keyword="机器学习",
        status=1,  # 1-待爬取
        priority=8
    )
```

#### 查询关键词

```python
# 根据关键词查询
keyword = await KeywordCRUD.get_by_keyword(session, "机器学习")

# 根据ID查询
keyword = await KeywordCRUD.get_by_id(session, keyword_id=1)

# 获取待爬取的关键词列表
pending = await KeywordCRUD.get_pending_keywords(session, limit=10)

# 获取所有关键词
all_keywords = await KeywordCRUD.get_all(
    session,
    status=1,  # 可选：筛选状态
    limit=100,
    offset=0,
    order_by="priority"  # 排序：created_at, priority, total_notes
)
```

#### 更新关键词

```python
from datetime import datetime

updated = await KeywordCRUD.update(
    session=session,
    keyword_id=1,
    status=2,  # 爬取中
    last_crawl_time=datetime.now()
)
```

#### 删除关键词

```python
success = await KeywordCRUD.delete(session, keyword_id=1)
```

### 笔记操作

#### 创建笔记

```python
from app.db import get_db_session, NoteCRUD
from datetime import datetime

async with get_db_session() as session:
    note = await NoteCRUD.create(
        session=session,
        keyword_id=1,
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
```

#### 批量创建笔记

```python
notes_data = [
    {
        "keyword_id": 1,
        "note_id": f"note_{i}",
        "title": f"Python教程第{i}篇",
        "content": f"这是第{i}篇Python教程的内容...",
        "author_id": f"author_{i}",
        "author_name": f"作者{i}",
        "like_count": 100 * i,
        "note_url": f"https://www.xiaohongshu.com/explore/{i}",
        "publish_time": datetime.now()
    }
    for i in range(100, 105)
]

created_notes = await NoteCRUD.batch_create(session, notes_data)
```

#### 查询笔记

```python
# 根据小红书笔记ID查询
note = await NoteCRUD.get_by_note_id(session, "note_123456789")

# 根据关键词ID查询笔记列表
notes = await NoteCRUD.get_by_keyword_id(
    session=session,
    keyword_id=1,
    limit=100,
    offset=0,
    order_by="like_count"  # crawl_time, like_count, publish_time
)

# 搜索笔记
notes = await NoteCRUD.search(
    session=session,
    keyword_id=1,  # 可选
    author_id="author_001",  # 可选
    min_like_count=500,  # 可选
    limit=100
)
```

#### 更新笔记

```python
updated = await NoteCRUD.update(
    session=session,
    note_id=1,
    like_count=2048,
    collect_count=512
)
```

### 评论操作

#### 创建评论

```python
from app.db import get_db_session, CommentCRUD

async with get_db_session() as session:
    comment = await CommentCRUD.create(
        session=session,
        note_id=1,
        comment_id="comment_001",
        content="这篇文章写得真好，学到了很多！",
        user_id="user_001",
        user_name="学习爱好者",
        user_avatar_url="minio://avatars/user_001.jpg",
        like_count=10,
        comment_time=datetime.now()
    )
```

#### 创建回复评论

```python
reply = await CommentCRUD.create(
    session=session,
    note_id=1,
    comment_id="comment_002",
    content="同感！我也觉得很有帮助",
    user_id="user_002",
    user_name="另一个用户",
    parent_comment_id="comment_001",  # 父评论ID
    like_count=5,
    comment_time=datetime.now()
)
```

#### 批量创建评论

```python
comments_data = [
    {
        "note_id": 1,
        "comment_id": f"comment_{i}",
        "content": f"这是第{i}条评论内容",
        "user_id": f"user_{i}",
        "user_name": f"用户{i}",
        "like_count": i * 2,
        "comment_time": datetime.now()
    }
    for i in range(10, 15)
]

created_comments = await CommentCRUD.batch_create(session, comments_data)
```

#### 查询评论

```python
# 根据笔记ID查询评论列表
comments = await CommentCRUD.get_by_note_id(
    session=session,
    note_id=1,
    limit=100,
    offset=0,
    order_by="like_count"  # comment_time, like_count
)

# 查询评论的回复
replies = await CommentCRUD.get_replies(
    session=session,
    parent_comment_id="comment_001",
    limit=50
)
```

## 按关键词查询爬取结果

```python
from app.db import get_db_session, KeywordCRUD, NoteCRUD, CommentCRUD

async with get_db_session() as session:
    # 1. 获取关键词
    keyword = await KeywordCRUD.get_by_keyword(session, "Python编程")
    
    # 2. 查询该关键词下的所有笔记
    notes = await NoteCRUD.get_by_keyword_id(
        session=session,
        keyword_id=keyword.id,
        limit=10,
        order_by="like_count"
    )
    
    # 3. 遍历笔记，查询评论
    for note in notes:
        print(f"笔记: {note.title}")
        print(f"点赞: {note.like_count}, 收藏: {note.collect_count}")
        
        # 查询该笔记的评论
        comments = await CommentCRUD.get_by_note_id(
            session=session,
            note_id=note.id,
            limit=10
        )
        print(f"评论数: {len(comments)}")
```

## 在FastAPI中使用

### 方式1：使用依赖注入

```python
from fastapi import Depends
from app.db import get_session
from app.db.crud import KeywordCRUD

@app.get("/keywords")
async def get_keywords(session: AsyncSession = Depends(get_session)):
    keywords = await KeywordCRUD.get_all(session, limit=100)
    return keywords
```

### 方式2：使用上下文管理器

```python
from app.db import get_db_session
from app.db.crud import KeywordCRUD

@app.post("/keywords")
async def create_keyword(keyword: str):
    async with get_db_session() as session:
        new_keyword = await KeywordCRUD.create(
            session=session,
            keyword=keyword
        )
        return new_keyword
```

## 注意事项

1. **事务管理**：使用 `get_db_session()` 会自动管理事务，成功时提交，异常时回滚。

2. **连接池**：数据库连接使用连接池管理，避免频繁创建连接。

3. **异步操作**：所有数据库操作都是异步的，必须在 `async` 函数中使用。

4. **唯一约束**：关键词、笔记ID、评论ID都有唯一约束，重复创建会抛出 `ValueError`。

5. **外键关联**：删除关键词或笔记时，关联的笔记或评论会自动删除（CASCADE）。

6. **日志记录**：所有操作都会记录日志，便于调试和监控。

## 完整示例

参考 `examples/db_usage_example.py` 文件查看完整的使用示例。

运行示例：

```bash
python examples/db_usage_example.py
```

