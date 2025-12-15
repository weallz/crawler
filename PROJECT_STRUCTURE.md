# 小红书爬虫项目目录结构说明

## 项目目录树

```
xiaohongshu_spider/
├── app/                          # 主应用目录
│   ├── __init__.py              # 应用包初始化文件
│   ├── api/                     # API接口模块
│   │   ├── __init__.py
│   │   └── v1/                  # API v1版本
│   │       ├── __init__.py
│   │       ├── endpoints/       # API端点（待开发）
│   │       └── routers.py       # 路由配置（待开发）
│   ├── core/                    # 核心配置模块
│   │   ├── __init__.py
│   │   ├── config.py            # 配置加载（待开发）
│   │   └── security.py          # 安全相关（待开发）
│   ├── crawler/                 # 爬虫模块
│   │   ├── __init__.py
│   │   ├── base.py              # 爬虫基类（待开发）
│   │   ├── xiaohongshu.py       # 小红书爬虫实现（待开发）
│   │   └── parsers.py           # 数据解析器（待开发）
│   ├── db/                      # 数据库模块
│   │   ├── __init__.py
│   │   ├── base.py              # 数据库基类（待开发）
│   │   ├── session.py           # 数据库会话管理（待开发）
│   │   └── migrations/          # 数据库迁移脚本（待开发）
│   ├── models/                  # 数据模型模块（SQLAlchemy ORM）
│   │   ├── __init__.py
│   │   ├── base.py              # 模型基类（待开发）
│   │   └── xiaohongshu.py       # 小红书数据模型（待开发）
│   ├── schemas/                 # 数据模式模块（Pydantic）
│   │   ├── __init__.py
│   │   ├── base.py              # 模式基类（待开发）
│   │   └── xiaohongshu.py       # 小红书数据模式（待开发）
│   ├── services/                # 业务服务模块
│   │   ├── __init__.py
│   │   ├── crawler_service.py   # 爬虫服务（待开发）
│   │   └── data_service.py      # 数据服务（待开发）
│   ├── storage/                 # 对象存储模块
│   │   ├── __init__.py
│   │   ├── base.py              # 存储基类（待开发）
│   │   └── minio_client.py      # MinIO客户端（待开发）
│   ├── tasks/                   # 异步任务模块
│   │   ├── __init__.py
│   │   ├── celery_app.py        # Celery应用配置（待开发）
│   │   └── crawler_tasks.py     # 爬虫异步任务（待开发）
│   ├── utils/                   # 工具类模块
│   │   ├── __init__.py
│   │   ├── logger.py            # 日志工具（待开发）
│   │   ├── decorators.py        # 装饰器（待开发）
│   │   └── helpers.py           # 辅助函数（待开发）
│   └── config/                  # 配置模块
│       ├── __init__.py
│       └── settings.py          # 配置设置（待开发）
├── logs/                        # 日志文件目录
├── tests/                       # 测试模块
│   ├── __init__.py
│   ├── test_crawler.py          # 爬虫测试（待开发）
│   └── test_api.py              # API测试（待开发）
├── .env.example                 # 环境配置模板文件
├── .env                         # 环境配置文件（需自行创建）
├── .gitignore                   # Git忽略文件（待创建）
├── requirements.txt             # Python依赖文件
├── main.py                      # 应用入口文件（待开发）
└── PROJECT_STRUCTURE.md         # 项目结构说明文档（本文件）
```

## 目录用途说明

### app/ - 主应用目录
整个项目的核心代码目录，包含所有业务逻辑模块。

### app/api/ - API接口模块
- **职责**: 处理HTTP请求和响应，定义RESTful API端点
- **说明**: 基于FastAPI框架，提供异步API接口，支持API版本管理（v1）

### app/core/ - 核心配置模块
- **职责**: 应用核心配置和安全相关功能
- **说明**: 包含配置加载、安全认证、中间件等核心功能

### app/crawler/ - 爬虫模块
- **职责**: 实现小红书数据爬取逻辑
- **说明**: 包含爬虫基类、具体爬虫实现、数据解析器等，支持异步IO

### app/db/ - 数据库模块
- **职责**: 数据库连接、会话管理、迁移脚本
- **说明**: 使用SQLAlchemy异步引擎，管理MySQL数据库连接池

### app/models/ - 数据模型模块
- **职责**: 定义数据库ORM模型
- **说明**: 使用SQLAlchemy定义数据表结构，对应数据库实体

### app/schemas/ - 数据模式模块
- **职责**: 定义API请求/响应的数据验证模式
- **说明**: 使用Pydantic定义数据验证和序列化模式

### app/services/ - 业务服务模块
- **职责**: 封装业务逻辑，协调各模块协作
- **说明**: 包含爬虫服务、数据服务等业务层代码

### app/storage/ - 对象存储模块
- **职责**: 处理文件存储，对接MinIO对象存储
- **说明**: 封装MinIO客户端，提供统一的存储接口

### app/tasks/ - 异步任务模块
- **职责**: 定义和管理异步后台任务
- **说明**: 使用Celery实现异步任务队列，处理耗时操作

### app/utils/ - 工具类模块
- **职责**: 提供通用工具函数和类
- **说明**: 包含日志工具、装饰器、辅助函数等

### app/config/ - 配置模块
- **职责**: 统一管理应用配置
- **说明**: 从环境变量加载配置，提供配置访问接口

### logs/ - 日志文件目录
- **职责**: 存储应用运行日志
- **说明**: 日志文件按日期和大小自动轮转

### tests/ - 测试模块
- **职责**: 单元测试和集成测试
- **说明**: 使用pytest框架编写测试用例

## 技术架构说明

### 异步IO架构
- **FastAPI**: 异步Web框架，提供高性能API服务
- **aiomysql**: 异步MySQL驱动，支持高并发数据库操作
- **httpx/aiohttp**: 异步HTTP客户端，用于爬虫请求
- **Celery**: 异步任务队列，处理后台任务

### 数据存储
- **MySQL**: 关系型数据库，存储结构化数据
- **MinIO**: 对象存储，存储图片、视频等文件
- **Redis**: 缓存和任务队列中间件

### 开发规范
- 遵循Python PEP 8编码规范
- 使用类型提示（Type Hints）
- 模块职责单一，便于维护和扩展
- 支持依赖注入和配置管理

## 后续开发建议

1. **配置加载**: 在 `app/config/settings.py` 中实现配置类，使用pydantic-settings加载.env配置
2. **数据库连接**: 在 `app/db/session.py` 中实现异步数据库会话管理
3. **爬虫实现**: 在 `app/crawler/` 中实现具体爬虫逻辑，支持反爬策略
4. **API开发**: 在 `app/api/v1/` 中定义RESTful API端点
5. **任务队列**: 在 `app/tasks/` 中配置Celery，实现异步任务处理
6. **日志系统**: 在 `app/utils/logger.py` 中配置loguru日志系统
