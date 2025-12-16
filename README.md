# 小红书爬虫项目

基于 FastAPI + 异步IO 的高性能小红书数据爬取与管理系统

## 📋 项目简介

本项目是一个功能完整的小红书数据爬虫系统，支持通过关键词批量爬取笔记、评论等数据。系统采用异步架构设计，提供 RESTful API 接口，支持任务调度和并发处理。爬取的数据结构化存储到 MySQL 数据库，媒体文件（图片/视频）存储到 MinIO 对象存储。

## ✨ 主要功能

- 🔍 **关键词爬取**：支持批量关键词搜索，自动爬取相关笔记
- 📝 **笔记数据**：爬取笔记标题、内容、作者、互动数据（点赞、收藏、评论、分享、浏览）
- 💬 **评论抓取**：支持抓取笔记评论及回复，可配置抓取数量
- 🖼️ **媒体存储**：自动将图片、视频上传至 MinIO 对象存储
- 📊 **数据持久化**：结构化数据存储到 MySQL 数据库，支持关联查询
- 🚀 **异步任务**：基于 asyncio 的异步任务调度系统，无需额外消息队列
- 🌐 **RESTful API**：提供完整的 API 接口，支持任务创建、查询、结果获取
- 📈 **并发控制**：支持自定义并发数和请求延迟，避免被封禁
- 🔄 **任务管理**：支持任务状态跟踪（待爬取、爬取中、已完成、已失败）

## 🛠️ 技术栈

### 后端框架
- **FastAPI** 0.115.0 - 高性能异步 Web 框架
- **Uvicorn** - ASGI 服务器
- **Pydantic** 2.9.2 - 数据验证和序列化

### 数据库
- **MySQL 8.1+** - 关系型数据库
- **SQLAlchemy** 2.0.36 - ORM 框架
- **aiomysql** 0.2.0 - 异步 MySQL 驱动

### 存储
- **MinIO** 7.2.6 - 对象存储服务
- **Redis** 5.2.0 - 缓存和任务队列（可选）

### 爬虫
- **aiohttp** 3.10.11 - 异步 HTTP 客户端
- **httpx** 0.27.2 - 异步 HTTP 库
- **BeautifulSoup4** 4.12.3 - HTML 解析
- **lxml** 5.3.0 - XML/HTML 解析器

### 其他
- **loguru** 0.7.2 - 日志系统
- **python-dotenv** 1.0.1 - 环境变量管理
- **asyncio** - 异步任务调度
- **python-dateutil** 2.9.0 - 时间处理

## 📁 项目结构

```
xiaohongshu_spider/
├── app/                          # 主应用目录
│   ├── api/                     # API接口模块
│   │   ├── router.py            # 路由定义
│   │   └── v1/                  # API v1版本
│   ├── crawler/                 # 爬虫模块
│   │   ├── xhs_spider.py       # 小红书爬虫核心
│   │   └── utils.py             # 工具函数（UA、文本清洗等）
│   ├── db/                      # 数据库模块
│   │   ├── conn.py              # 数据库连接和会话管理
│   │   ├── models.py            # ORM模型（Keyword, Note, Comment）
│   │   └── crud.py              # CRUD操作
│   ├── storage/                 # 对象存储模块
│   │   └── minio_client.py      # MinIO异步客户端
│   ├── task/                    # 任务调度模块
│   │   └── async_scheduler.py   # 异步任务调度器
│   ├── config/                  # 配置模块
│   ├── core/                    # 核心配置模块
│   ├── models/                  # 数据模型模块
│   ├── schemas/                 # 数据模式模块（Pydantic）
│   ├── services/                # 业务服务模块
│   └── utils/                   # 工具类模块
├── data/                        # 数据目录
│   ├── README.md                # 数据目录说明
│   └── notes/                   # 笔记数据目录
│       ├── result_note.md       # 爬取的笔记数据（Markdown 格式）
│       └── bug.md               # 爬虫过程中遇到的问题及解决方案记录
├── db/                          # 数据库脚本
│   └── schema.sql               # 数据库表结构定义
├── docs/                        # 文档目录
│   ├── database_module_summary.md
│   ├── database_module_usage.md
│   └── minio_exception_handling.md
├── examples/                    # 示例代码
│   ├── db_usage_example.py     # 数据库使用示例
│   └── minio_usage_example.py  # MinIO使用示例
├── tests/                       # 测试目录
├── logs/                        # 日志目录
├── main.py                      # FastAPI应用入口
├── run_crawler.py               # 爬虫直接运行脚本
├── test_image_upload.py         # 图片上传功能测试
├── requirements.txt             # Python依赖文件
├── env.example                  # 环境变量配置示例
├── PROJECT_STRUCTURE.md         # 项目结构说明文档
└── README.md                    # 项目说明文档（本文件）
```

## 🚀 快速开始

### 环境要求

- **Python** 3.13.2+
- **MySQL** 8.1+
- **MinIO**（可选，用于对象存储）
- **Redis**（可选，用于缓存）

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd xiaohongshu_spider
```

2. **创建虚拟环境**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
# 复制环境变量示例文件
cp env.example .env

# 编辑 .env 文件，配置数据库、MinIO等信息
# Windows 使用 notepad .env
# Linux/Mac 使用 vim .env 或 nano .env
```

5. **初始化数据库**
```bash
# 登录 MySQL
mysql -u root -p

# 执行数据库脚本
source db/schema.sql

# 或者直接导入
mysql -u root -p < db/schema.sql
```

6. **启动 MinIO（可选）**
```bash
# 使用 Docker 启动 MinIO
docker run -d \
  -p 9000:9000 \
  -p 9001:9001 \
  --name minio \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  minio/minio server /data --console-address ":9001"
```

7. **启动服务**
```bash
# 启动 API 服务
python main.py

# 或使用 uvicorn（支持热重载）
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

8. **访问 API 文档**
```
http://localhost:8000/docs          # Swagger UI
http://localhost:8000/redoc        # ReDoc
http://localhost:8000/health       # 健康检查
```

## ⚙️ 配置说明

### 环境变量配置

主要配置项（详见 `env.example`）：

```env
# ============================================
# 数据库配置 (MySQL 8.1+)
# ============================================
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=xiaohongshu_spider
DB_CHARSET=utf8mb4

# 数据库连接池配置
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
DB_ECHO=false                    # 是否打印SQL语句

# ============================================
# MinIO对象存储配置
# ============================================
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_SECURE=false               # 是否使用HTTPS
MINIO_BUCKET_NAME=xiaohongshu

# ============================================
# Redis配置（可选）
# ============================================
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# ============================================
# 日志配置
# ============================================
LOG_LEVEL=INFO
LOG_FILE=logs/xiaohongshu_spider.log

# ============================================
# 爬虫配置
# ============================================
CRAWLER_CONCURRENT=5             # 并发数
CRAWLER_DELAY=1                  # 请求延迟（秒）
CRAWLER_TIMEOUT=30               # 请求超时（秒）
XHS_COOKIES=your_cookies_here    # 小红书Cookie（可选，提升稳定性）
COMMENT_LIMIT=20                 # 每条笔记最多抓取评论数

# ============================================
# 任务调度配置
# ============================================
SCHEDULER_CONCURRENCY=3          # 调度器并发数
SCHEDULER_POLL_INTERVAL=2        # 轮询间隔（秒）

# ============================================
# API配置
# ============================================
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true                  # 开发环境热重载
```

## 📖 使用指南

### 1. 通过 API 创建爬取任务

```bash
curl -X POST "http://localhost:8000/api/crawl/task" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["美食", "旅游", "穿搭"],
    "note_limit": 50
  }'
```

响应示例：
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "created": ["美食", "旅游", "穿搭"],
    "skipped": []
  }
}
```

### 2. 查询任务列表

```bash
curl "http://localhost:8000/api/crawl/keywords"
```

响应示例：
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "tasks": [
      {
        "keyword": "美食",
        "status": "running",
        "note_limit": 50,
        "error": null
      }
    ]
  }
}
```

### 3. 获取爬取结果

```bash
curl "http://localhost:8000/api/crawl/result?keyword=美食"
```

响应示例：
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "keyword": "美食",
    "notes": [
      {
        "note_id": "xxx",
        "title": "美食推荐",
        "desc": "这是一篇美食笔记...",
        "liked": 1000,
        "collected": 500,
        "commented": 200,
        "publish_time": "2024-01-01T00:00:00",
        "images": ["url1", "url2"],
        "comments": [...]
      }
    ]
  }
}
```

### 4. 直接运行爬虫脚本

```bash
# 设置环境变量
export XHS_KEYWORD="美食"
export XHS_PER_KEYWORD=50

# 运行爬虫
python run_crawler.py
```

### 5. 测试图片上传功能

```bash
python test_image_upload.py
```

### 6. 使用数据库操作示例

```bash
python examples/db_usage_example.py
```

### 7. 使用 MinIO 存储示例

```bash
python examples/minio_usage_example.py
```

## 📊 数据库结构

### 关键词表 (keywords)
存储待爬取的关键词及状态信息。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键ID |
| keyword | VARCHAR(255) | 关键词（唯一） |
| status | TINYINT | 状态：1-待爬取，2-爬取中，3-已完成，4-已失败 |
| priority | INT | 优先级（数字越大优先级越高） |
| total_notes | BIGINT | 已爬取笔记总数 |
| last_crawl_time | DATETIME | 最后爬取时间 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 笔记表 (notes)
存储笔记基本信息、作者信息、互动数据。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键ID |
| keyword_id | BIGINT | 关联关键词ID（外键） |
| note_id | VARCHAR(100) | 小红书笔记ID（唯一） |
| title | VARCHAR(500) | 笔记标题 |
| content | TEXT | 笔记正文内容 |
| author_id | VARCHAR(100) | 作者ID |
| author_name | VARCHAR(255) | 作者昵称 |
| author_avatar_url | VARCHAR(500) | 作者头像URL（MinIO） |
| like_count | INT | 点赞数 |
| collect_count | INT | 收藏数 |
| comment_count | INT | 评论数 |
| share_count | INT | 分享数 |
| view_count | INT | 浏览量 |
| cover_image_url | VARCHAR(500) | 封面图片URL（MinIO） |
| image_urls | JSON | 笔记图片URL列表（JSON格式） |
| video_url | VARCHAR(500) | 视频URL（MinIO） |
| note_url | VARCHAR(500) | 笔记原始链接 |
| publish_time | DATETIME | 发布时间 |
| crawl_time | DATETIME | 爬取时间 |

### 评论表 (comments)
存储评论内容、用户信息，支持回复评论。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键ID |
| note_id | BIGINT | 关联笔记ID（外键） |
| comment_id | VARCHAR(100) | 评论ID（小红书唯一标识） |
| parent_comment_id | VARCHAR(100) | 父评论ID（用于回复评论） |
| user_id | VARCHAR(100) | 评论用户ID |
| user_name | VARCHAR(255) | 评论用户昵称 |
| user_avatar_url | VARCHAR(500) | 评论用户头像URL（MinIO） |
| content | TEXT | 评论内容 |
| like_count | INT | 评论点赞数 |
| reply_count | INT | 回复数 |
| comment_time | DATETIME | 评论时间 |
| crawl_time | DATETIME | 爬取时间 |

## 🔌 API 接口文档

### 创建爬取任务
- **URL**: `POST /api/crawl/task`
- **请求体**:
```json
{
  "keywords": ["关键词1", "关键词2"],
  "note_limit": 50
}
```
- **响应**: 返回创建和跳过的关键词列表

### 查询任务列表
- **URL**: `GET /api/crawl/keywords`
- **响应**: 返回所有任务的状态信息

### 获取爬取结果
- **URL**: `GET /api/crawl/result?keyword=关键词`
- **响应**: 返回指定关键词的爬取结果

### 健康检查
- **URL**: `GET /health`
- **响应**: 返回服务状态

### API 文档
- **Swagger UI**: `GET /docs`
- **ReDoc**: `GET /redoc`

## 🧪 测试

```bash
# 运行测试（待实现）
pytest tests/

# 测试图片上传
python test_image_upload.py

# 测试数据库连接
python -c "from app.db.conn import check_db_connection; import asyncio; asyncio.run(check_db_connection())"
```

## 📝 开发说明

### 代码规范
- 遵循 **PEP 8** 编码规范
- 使用 **类型提示（Type Hints）**
- 模块职责单一，便于维护和扩展
- 使用 **loguru** 进行统一日志记录

### 日志系统
- 日志文件存储在 `logs/` 目录
- 支持日志级别配置（DEBUG, INFO, WARNING, ERROR）
- 日志自动轮转，避免文件过大

### 异步处理
- 爬虫采用异步IO，支持高并发
- 任务调度基于 asyncio，无需额外消息队列
- 数据库操作使用异步SQLAlchemy

### 数据库操作
- 使用 SQLAlchemy 2.0+ 异步API
- 支持连接池管理，提高性能
- 提供完整的 CRUD 操作类

### 对象存储
- MinIO 客户端支持异步操作
- 自动创建存储桶
- 支持预签名URL生成

## 📁 数据目录说明

项目包含一个 `data/` 目录，用于存放爬取的结果数据：

- `data/notes/` - 存放爬取的笔记数据，以 Markdown 格式保存
- `data/notes/bug.md` - 记录爬虫过程中遇到的问题及解决方案

数据目录已在 `.gitignore` 中被忽略，不会提交到版本控制系统中。

## ⚠️ 注意事项

1. **合规使用**：请遵守小红书的服务条款，合理使用爬虫功能，避免对服务器造成过大压力
2. **请求频率**：建议设置适当的延迟（`CRAWLER_DELAY`），避免请求过于频繁
3. **Cookie配置**：配置有效的 Cookie（`XHS_COOKIES`）可以提升爬取稳定性和成功率
4. **数据存储**：确保 MySQL 和 MinIO 服务正常运行，数据库表已创建
5. **反爬策略**：小红书可能有反爬机制，需要根据实际情况调整策略（UA、延迟、Cookie等）
6. **数据过滤**：系统会自动过滤非图文笔记和6个月前的笔记，可在代码中调整过滤条件
7. **评论限制**：默认每条笔记最多抓取20条评论，可通过 `COMMENT_LIMIT` 配置

## 🔧 常见问题

### Q: 数据库连接失败？
A: 检查 `.env` 文件中的数据库配置是否正确，确保 MySQL 服务已启动，数据库已创建。

### Q: MinIO 上传失败？
A: 检查 MinIO 服务是否运行，配置是否正确，存储桶是否已创建。

### Q: 爬取失败或返回空数据？
A: 检查 Cookie 是否有效，请求频率是否过高，网络连接是否正常。

### Q: 如何查看日志？
A: 日志文件位于 `logs/` 目录，也可以通过控制台查看实时日志。

## 📄 许可证

[待添加]

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

[待添加]

---

**注意**：本项目仅供学习交流使用，请遵守相关法律法规和平台服务条款，勿用于商业用途或违反相关规定的行为。
