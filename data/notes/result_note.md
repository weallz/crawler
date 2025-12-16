# 小红书爬虫项目开发文档

## 阶段一：工程化基础框架

### 给cursor提示词命令

请基于Python完成小红书爬虫项目的工程化基础搭建，严格遵循以下要求输出内容：

1. 设计项目目录结构

- 基于FastAPI+异步IO架构，拆分爬虫、数据库、对象存储、API接口、异步任务、工具类等模块，要求目录层级清晰、每个模块职责单一，禁止冗余目录。

- 输出格式为“树形结构+目录用途说明”。

2. 生成requirements.txt文件

- 包含FastAPI、异步数据库、MinIO、异步爬虫、环境配置等核心依赖，标注具体版本号（需适配Python 3.9+），避免无用依赖。

3. 生成.env配置模板文件

- 包含MySQL数据库、MinIO对象存储、爬虫反爬（请求延迟、爬取数量）等配置项，用占位符标注需替换的内容，配置项命名规范且附带注释。

4. 代码/配置规范约束

- requirements.txt中的依赖需按功能分类（如Web框架、数据库、爬虫、存储）；

- .env模板中的配置项需区分模块，添加详细注释说明用途；

- 目录结构需符合Python工程化开发规范，便于后续分模块开发。

1. 设计项目目录结构

- 基于FastAPI+异步IO架构，拆分爬虫、数据库、对象存储、API接口、异步任务、工具类等模块，要求目录层级清晰、每个模块职责单一，禁止冗余目录。

- 输出格式为“树形结构+目录用途说明”。

2. 生成requirements.txt文件

- 包含FastAPI、异步数据库、MinIO、异步爬虫、环境配置等核心依赖，标注具体版本号（需适配Python 3.13.2），避免无用依赖。

3. 生成.env配置模板文件

- 包含MySQL数据库、MinIO对象存储、爬虫反爬（请求延迟、爬取数量）等配置项，用占位符标注需替换的内容，配置项命名规范且附带注释。

4. 代码/配置规范约束

- requirements.txt中的依赖需按功能分类（如Web框架、数据库、爬虫、存储）；

- .env模板中的配置项需区分模块，添加详细注释说明用途；

- 目录结构需符合Python工程化开发规范，便于后续分模块开发。

### 1.1 验证目录结构

（无具体操作步骤，仅需确认目录结构合规）

### 1.2 验证requirements.txt兼容性

1. 打开终端，进入项目根目录

2. 执行命令：`pip install -r requirements.txt`

3. 无报错即通过；若报错，复制错误信息给Cursor，让它调整依赖版本。
   
   ### 1.3 验证.env配置项
   
   打开 `.env` 文件，检查是否包含以下配置项（需带注释说明），有则通过：
- DB_HOST / MINIO_ACCESS_KEY / REQUEST_DELAY 等核心配置
  
  ```env
  # 应用名称
  APP_NAME=xiaohongshu_spider
  # 应用环境:development, production, testing
  APP_ENV=development
  # 应用调试模式:true, false
  DEBUG=true
  # API服务端口
  API_PORT=8000
  # API服务主机地址
  API_HOST=0.0.0.0
  # MySQL数据库配置
  # 数据库主机地址
  DB_HOST=localhost
  # 数据库端口
  DB_PORT=3306
  # 数据库名称
  DB_NAME=xiaohongshu_db
  # 数据库用户名
  DB_USER=root
  # 数据库密码
  DB_PASSWORD=123456
  # 数据库字符集
  DB_CHARSET=utf8mb4
  # 数据库连接池最小连接数
  DB_POOL_MIN_SIZE=5
  # 数据库连接池最大连接数
  DB_POOL_MAX_SIZE=20
  # 数据库连接超时时间(秒)
  DB_POOL_TIMEOUT=30
  # MinIO对象存储配置
  # MinIO服务端点地址
  MINIO_ENDPOINT=localhost:9000
  # MinIO访问密钥ID
  MINIO_ACCESS_KEY=your_minio_access_key
  # MinIO访问密钥
  MINIO_SECRET_KEY=your_minio_secret_key
  # 爬虫配置
  CRAWLER_DELAY_RANGE=1.0,3.0
  # 单次爬取最大数量
  CRAWLER_MAX_COUNT=100
  # 请求超时时间(秒)
  CRAWLER_TIMEOUT=30
  # 请求重试次数
  CRAWLER_RETRY_TIMES=3
  # 请求重试延迟(秒)
  CRAWLER_RETRY_DELAY=5
  # User-Agent轮换开关:true, false
  CRAWLER_ROTATE_USER_AGENT=true
  # 代理开关:true, false
  CRAWLER_USE_PROXY=false
  # 代理地址(如使用代理,格式:http://ip:port)
  CRAWLER_PROXY_URL=
  # 并发请求数
  CRAWLER_CONCURRENT_REQUESTS=5
  ```
  
  ## 阶段二：异步数据库模块
  
  ### 给cursor输入提示词
  
  请基于Python为小红书爬虫项目开发异步数据库模块，严格遵循以下要求输出代码和说明：
  
  1. 技术栈约束
  
  - 使用SQLAlchemy 2.0+异步版+aiomysql实现，适配Python 3.13.2，数据库为MySQL 8.1+。
  
  2. 表结构设计
  
  - 设计关键词表、笔记表、评论表，字段需包含爬虫需求的核心数据（关键词、笔记标题/文案/点赞/收藏/评论数、评论内容、MinIO图片URL等），需考虑外键关联、字段类型合理性、唯一约束。
  
  3. 代码开发要求
  
  - 按Python工程化规范拆分文件： db/conn.py （数据库连接）、 db/models.py （数据模型）、 db/crud.py （基础CRUD操作）；
  
  - 实现关键词、笔记、评论的异步增删改查核心方法（如新增关键词、批量插入笔记、按关键词查询爬取结果等）；
  
  - 代码遵循PEP8规范，添加函数/类注释，包含异常处理和日志记录；
  
  - 读取 .env 文件中的数据库配置，避免硬编码。
  
  4. 输出内容
  
  - 先输出MySQL建表SQL语句，再输出各文件的完整代码，最后附带代码使用示例（如异步新增关键词、查询笔记数据）。
  
  ### 2.1 创建数据库表
  
  在MySQL客户端执行建表SQL，创建3张核心表：
  
  | 表名       | 字段说明                                                                                                                                                                                        |
  | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | comments | id: bigint UNSIGNED、note_id: bigint UNSIGNED、comment_id: varchar(100)、parent_comment_id: varchar(100)、user_id: varchar(100)、user_name: varchar(255)、user_avatar_url: varchar(500)、更多(7列)... |
  | keywords | id: bigint UNSIGNED、keyword: varchar(255)、status: tinyint、priority: int、total_notes: int UNSIGNED、last_crawl_time: datetime、created_at: datetime、updated_at: datetime                       |
  | notes    | id: bigint UNSIGNED、keyword_id: bigint UNSIGNED、note_id: varchar(100)、title: varchar(500)、content: text、author_id: varchar(100)、author_name: varchar(255)、更多(14列)...                        |
  
  ### 2.2 验证数据库连接与CRUD功能
  
  运行脚本：`python examples/db_usage_example.py`

- 脚本运行无报错

- 打印出关键词信息，说明链接和CRUD功能正常
  **运行日志示例**：
  
  ```
  PS C:\Users\31241\xiaohongshu_spider> python examples/db_usage_example.py
  数据库模块使用示例
  1.检查数据库连接
  2025-12-15 14:58:45.960|INFO|app.db.conn:create_engine:145 - Database engine created: localhost:3306/xiaohongshu_spider (pool_size=10, max_overflow=20)
  2025-12-15 14:58:46.079|INFO|app.db.conn:check_db_connection:317 - Database connection check passed
  数据库连接成功
  2.初始化数据库
  2025-12-15 14:58:46.116|INFO|app.db.conn:init_db:268 - Database tables created successfully
  数据库表创建成功
  关键词操作示例
  1.创建关键词
  2025-12-15 14:58:46.213|INFO|app.db.crud:create:61 - 创建关键词成功:Python编程(ID:1)
  创建成功:<Keyword(id=1, keyword='Python编程', status=1)>
  2025-12-15 14:58:46.232|INFO|app.db.crud:create:61 - 创建关键词成功:机器学习(ID:2)
  创建成功:<Keyword(id=2, keyword='机器学习', status=1)>
  2.查询关键词
  查询结果:<Keyword(id=1, keyword='Python编程', status=1)>
  3.获取待爬取的关键词列表
  待爬取关键词数量:2
  4.示例笔记数据
  2.Python教程第103篇
  作者:作者1
  点赞:10300|收藏:2060|评论:1030
  发布时间:2025-12-15 14:58:46
  3.Python教程第102篇
  作者:作者0
  点赞:10200|收藏:2040|评论:1020
  发布时间:2025-12-15 14:58:46
  4.Python教程第101篇
  作者:作者2
  点赞:10100|收藏:2020|评论:1010
  5.Python教程第100篇
  作者:作者1
  点赞:10000|收藏:2000|评论:1000
  发布时间:2025-12-15 14:58:46
  6.Python异步编程入门
  作者:Python开发者
  点赞:2048|收藏:512|评论:128
  发布时间:2025-12-15 14:58:46
  评论(5条):
  1.学习爱好者:这篇文章写得真好,学到了很多!...
  2.另一个用户:同感!我也觉得很有帮助...
  3.用户10:这是第10条评论内容...
  4.关闭数据库连接
  2025-12-15 14:58:46.708|INFO|app.db.conn:close_db:283 - Database connections closed
  数据库连接已关闭
  ```
  
  ## 阶段三：MinIO存储模块
  
  ### 给cursor输入提示词
  
  ```
  
  ```

- 使用minio官方Python客户端,适配异步IO架构,需结合asyncio实现无阻塞文件操作,兼容Python 3.13.2。
  2.核心功能要求

- 实现图片/视频文件上传:支持本地临时文件上传至MinIO指定存储桶,自动生成唯一文件名(避免重复);

- 实现文件URL获取:生成带访问权限的文件链接,用于存入MySQL数据库;

- 实现存储桶检查/创建:初始化时自动检测目标存储桶是否存在,不存在则自动创建;

- 读取.env文件中的MinIO配置(endpoint、access key、secret key、bucket name、secure),禁止硬编码。
  3.代码开发规范

- 按工程化拆分文件: storage/minio_client.py (MinIO工具类)、storage/__init__.py(模块导出);

- 工具类需封装为AsyncMinioClient,方法名简洁语义化(如upload_file、get_file_url);

- 加入异常处理(如连接失败、上传超时、存储桶权限不足)和日志记录;

- 遵循PEP8规范,添加类/方法注释,说明参数和返回值。
  4.输出内容

- 完整的工具类代码;

- 代码使用示例(如异步上传一张本地图片、获取其URL);

- 常见异常解决方案(如MinioException处理)。
  ```
  
  ### 3.1 验证MinIO连接
  
  创建测试文件 `scripts.py`，执行命令：`python script.py`

- 输出存储桶创建成功日志即通过
  **运行日志示例**：
  
  ```
  C:\Users\31241\xiaohongshu_spider>python script.py
  MinIO client initialized: endpoint=localhost:9000, bucket=xiaohongshu-storage
  2025-12-15 16:05:14.260|INFO|app.storage.minio_client:check_and_create_bucket:87 - Bucket xiaohongshu-storage does not exist, creating...
  2025-12-15 16:05:14.288|INFO|app.storage.minio_client:check_and_create_bucket:92 - Bucket xiaohongshu-storage created successfully
  2025-12-15 16:05:14.288|INFO|app.storage.minio_client:check_and_create_bucket:94 - Bucket xiaohongshu-storage is ready
  Bucket OK
  2025-12-15 16:05:14.290|DEBUG|app.storage.minio_client:get_file_url:173 - Generated presigned URL for health-check-placeholder
  Presigned URL generated: http://localhost:9000/xiaohongshu-storage/health-check-placeholder?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20251215%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20251215T080514Z&X-Amz-Expires=60&X-Amz-SignedHeaders=host&X-Amz-Signature=0eef384e95034bd0e6bcbfc24407c1e17d3bb4b0b675bb0b9e317778170db938
  ```
  
  ### 3.2 验证文件上传与访问
  
  运行测试脚本 `test_image_upload.py`，执行命令：`python test_image_upload.py`

- 图片上传成功

- 生成的URL可在浏览器打开

- MinIO控制台可查看上传文件
  **运行日志示例**：
  
  ```
  PS C:\Users\31241\xiaohongshu_spider> python test_image_upload.py
  小红书爬虫项目-图片上传功能测试
  开始测试图片上传功能...
  2025-12-15 16:13:33.669|INFO|app.storage.minio_client:__init__:53 - MinIO client initialized: endpoint=localhost:9000, bucket=xiaohongshu-storage
  检查存储桶...
  2025-12-15 16:13:33.713|INFO|app.storage.minio_client:check_and_create_bucket:94 - Bucket xiaohongshu-storage is ready
  √ 存储桶检查完成
  创建测试图片文件...
  √ 测试图片创建完成:C:\Users\31241\AppData\Local\Temp\tmpxxesz7f3.png
  上传图片...
  2025-12-15 16:13:33.796|INFO|app.storage.minio_client:upload_file:141 - File uploaded successfully: c:\users\31241\AppData\Local\Temp\tmpxxesz7f3.png -> test-image.png
  √ 图片上传成功,对象名:test-image.png
  生成访问URL...
  2025-12-15 16:13:33.799|DEBUG|app.storage.minio_client:get_file_url:173 - Generated presigned URL for test-image.png
  √ URL生成成功: http://localhost:9000/xiaohongshu-storage/test-image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20251215%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20251215T081333Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=6eaf9adbf87e4b6b58b9f14bf9d2fd25f7af8e748f6fcb3fa9071041fa3b4b02
  测试URL可访问性...
  √ URL可正常访问
  2025-12-15 16:13:33.815|INFO|app.storage.minio_client:close:186 - MinIO client closed
  2025-12-15 16:13:33.815|INFO|app.storage.minio_client:close:186 - MinIO client closed
  检查存储桶内容...
  2025-12-15 16:13:33.820|INFO|app.storage.minio_client:__init__:53 - MinIO client initialized: endpoint=localhost:9000, bucket=xiaohongshu-storage
  存储桶'xiaohongshu-storage'中的对象:
  test-image.png (69 bytes, 2025-12-15 08:13:33.773000+00:00)
  总共1个对象
  2025-12-15 16:13:33.879|INFO|app.storage.minio_client:close:186 - MinIO client closed
  ```
  
  **MinIO控制台验证**：
  访问 `localhost:9001/browser/xiaohongshu-storage/`，可看到 `test-image.png` 文件（69.0B，创建时间为测试时间）
  
  ## 阶段四：异步爬虫核心模块
  
  ### 给cursor输入提示词
  
  ```
  
  ```

- 使用aiohttp实现异步HTTP请求,结合asyncio调度任务,适配Python 3.13.2+,禁止使用同步爬虫库(如requests)。
  2.核心功能要求

- 关键词适配:支持接收多个关键词(50-100个),每个关键词可配置爬取笔记数量(默认50条);

- 数据爬取范围:仅爬取半年内、评论量最高的图文笔记(过滤视频笔记/广告笔记);

- 提取字段:笔记ID、标题、文案、点赞量、收藏量、评论量、发布时间、所有图片(不含视频)、前20条评论内容;

- 反爬机制:实现请求头伪装(User-Agent随机切换)、请求延迟(可通过.env配置,默认1秒)、Cookie适配(支持传入小红书Cookie,提升爬取稳定性);

- 数据预处理:清洗笔记文案中的特殊字符,处理图片URL去重,格式化发布时间为datetime格式。
  3.代码开发规范

- 按工程化拆分文件:crawler/xhs_spider.py(核心爬虫类)、crawler/utils.py(工具函数,如请求头生成、数据清洗)、crawler/__init__.py(模块导出);

- 核心类封装为AsyncXhsCrawler,方法语义化(如fetch_notes_by_keyword、extract_note_data、fetch_comments);

- 加入异常处理(如请求失败重试、数据解析失败跳过、网络超时处理)和详细日志记录(记录爬取进度、失败原因);

- 读取.env中的爬虫配置(请求延迟、评论爬取上限),禁止硬编码。
  4.输出内容

- 完整的爬虫类代码+工具函数代码;

- 代码使用示例(如异步爬取"美食"关键词的50条笔记,提取所有字段);

- 反爬优化说明(如Cookie获取方式、请求频率调整建议)。
  
  ```
  ### 4.1 测试爬虫脚本
  在根目录创建测试脚本 `run_crawler.py`，执行命令：`python run_crawler.py`
  **运行日志示例**（Cookie失效场景）：
  ```
  
  PS C:\Users\31241\xiaohongshu_spider> python run_crawler.py
  2025-12-15 16:41:27.609|MARNING|app.crawler.xhs_spider:_request_json:74 - Request failed %s status=%s
  2025-12-15 16:41:27.611|INFO|app.crawler.xhs_spider:fetch_notes_by_keyword:118 - keyword=%s fetched=%d
  关键词:美食 返回条数:0
  
  ```
  ## 阶段五：FastAPI接口+异步任务调度
  ### 给cursor输入提示词
  ```
  
  请基于Python为小红书爬虫项目开发FastAPI接口+异步任务调度模块,严格遵循以下要求输出代码和说明:
  1.技术栈约束

- 使用FastAPI搭建RESTful接口,结合asyncio实现数据库轮询式生产者-消费者异步任务调度,不依赖消息队列中间件,适配Python 3.9+。
  2.核心功能要求
  异步任务调度:
1. 生产者:接收关键词爬取任务后,将关键词写入数据库并标记状态为"爬取中";
2. 消费者:后台异步轮询数据库,获取待爬取关键词,调用AsyncXhsCrawler执行爬取,爬取完成后更新状态为"爬取完成/失败";
3. 支持并发爬取(可通过.env配置并发数),避免重复爬取同一关键词。
   接口开发:实现3个核心RESTful接口,包含参数校验、异常处理、统一JSON响应格式:
4. POST /api/crawl/task: 接收JSON参数 {"keywords":["美食","旅行"], "note_limit": 50},触发爬取任务;
5. GET /api/crawl/keywords:查询所有关键词及其爬取状态;
6. GET /api/crawl/result:接收查询参数keyword,返回该关键词下的笔记、评论、图片URL等完整数据。
- 配置读取:读取.env中的接口端口、并发数等配置,禁止硬编码。
  3.代码开发规范

- 按工程化拆分文件:api/router.py(接口路由)、task/async_scheduler.py(异步任务调度)、main.py(项目入口);

- 接口添加请求模型(Pydantic)做参数校验,统一响应格式为{"code": 200, "msg":"success", "data":{...}};

- 加入日志记录(记录接口请求、任务调度、爬取状态)和异常处理(如参数错误、任务重复、爬取失败);

- 遵循PEP8规范,添加类/方法注释,说明参数和返回值。
  4.输出内容

- 完整的路由、任务调度、项目入口代码;

- 接口测试示例(curl命令或Swagger使用步骤);

- 任务调度逻辑说明(生产者-消费者如何通过数据库轮询协作)。
  ```
  
  ### 5.1 验证服务启动
  
  执行命令：`python main.py`

- 终端提示 `running on http://127.0.0.1:8000` 即通过
  **启动日志示例**：
  
  ```
  C:\Users\31241\xiaohongshu_spider>python main.py
  C:\Users\31241\xiaohongshu_spider\main.py:29: DeprecationWarning: on_event is deprecated, use lifespan event handlers instead.
  Read more about it in the [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
  @app.on_event("startup")
  C:\Users\31241\xiaohongshu_spider\main.py:35: DeprecationWarning: on_event is deprecated, use lifespan event handlers instead.
  Read more about it in the [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
  @app.on_event("shutdown")
  INFO: Started server process [27608]
  INFO: Waiting for application startup.
  2025-12-15 16:53:42.509|INFO|app.task.async_scheduler:start:90 - Task scheduler started with concurrency=%s
  2025-12-15 16:53:42.509|INFO|main:_startup:32 - scheduler started
  INFO: Application startup complete.
  INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
  INFO: 127.0.0.1:59968 - "GET /docs HTTP/1.1" 200 OK
  ```
  
  **访问根路径验证**：
  打开浏览器访问 `http://localhost:8000`，返回以下JSON即通过：
  
  ```json
  {"message":"小红书爬虫API服务", "version":"1.0.0", "docs":"/docs"}
  ```
  
  ### 5.2 验证Swagger文档
  
  打开浏览器访问 `http://localhost:8000/docs`，能看到3个核心接口即通过：

- POST /api/crawl/task

- GET /api/crawl/keywords

- GET /api/crawl/result
  
  ### 5.3 验证异步任务与查询接口
  
  #### 5.3.1 触发爬取任务
1. 在Swagger页面点击 `POST /api/crawl/task` → Try it out

2. 输入请求参数：
   
   ```json
   {
   "keywords": ["美食"],
   "note_limit": 5
   }
   ```

3. 点击 Execute，返回 `code:200` 即通过
   **响应示例**：
   
   ```json
   {
   "code": 200,
   "msg": "success",
   "data": {
   "created": ["美食"],
   "skipped": []
   }
   }
   ```
   
   **Curl命令示例**：
   
   ```bash
   curl -X 'POST' \
   'http://127.0.0.1:8000/api/crawl/task' \
   -H 'accept: application/json' \
   -H 'Content-Type: application/json' \
   -d '{
   "keywords": ["美食"],
   "note_limit": 5
   }'
   ```
   
   #### 5.3.2 查询爬取结果

4. 点击 `GET /api/crawl/result` → Try it out

5. 输入查询参数 `keyword: 美食`

6. 点击 Execute，返回包含笔记和评论数据的JSON即通过
   **响应示例**：
   
   ```json
   {
   "code": 200,
   "msg": "success",
   "data": {
   "keyword": "美食",
   "notes": [
   // 笔记详情+评论数据
   ]
   }
   }
   ```
   
   **Curl命令示例**：
   
   ```bash
   curl -X 'GET' \
   'http://127.0.0.1:8000/api/crawl/result?keyword=%E7%BE%8E%E9%A3%9F' \
   -H 'accept: application/json'
   ```
