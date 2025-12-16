### 运行报错及解决方案记录

#### 1. 模块导入错误

```bash
C:\Users\31241\xiaohongshu_spider>python examples/db_usage_example.py
Traceback (most recent call last):
File "c:\Users\31241\xiaohongshu_spider\examples\db_usage_example.py", line 9, in <module>
from app.db import(
...<7 lines>...
ModuleNotFoundError: No module named 'app'
```

**解决方案**：添加项目根目录到 Python 路径

```python
import sys
from pathlib import Path
# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
```

#### 2. 日志写入相关代码

```python
def __repr__(self) -> str:
 # #region agent log
 try:
 with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log','a',encoding='utf-8') as f:
 f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix","hypothesis":""}))
 except:
 pass
 # #endregion
 return f"<Note(id={self.id}, note_id='{self.note_id}', title='{self.title[:30]}...')>"
```

#### 3. 数据库字符集配置问题

**问题**：数据库字符集未正确选择
**配置步骤**：
4. 在弹出的对话框中：

- 数据库名输入：`xiaohongshu_spider`
- 字符集选择：`utf8mb4`
- 排序规则选择：`utf8mb4_unicode_ci`
  
  #### 4. MinIO 安装与配置问题
  
  **问题**：MinIO 未下载，使用 Docker 安装时国内镜像加速器无法拉取
  - ```bash
    C:\Users\31241\xiaohongshu_spider>python script.py
    2025-12-15 15:42:02.572|INFO | app.storage.minio_client:_init_:53 - Minio client initialized: endpoint=localhost:9000, bucket=xiaohongshu-storage
    MinIO check failed: 'AsyncMinioClient' object has no attribute 'ensure_bucket'
    ```
    
    **解决方案**：
    - 更换镜像源：`docker.1ms.run`
    - 修改 `.env` 文件配置
    - 成功初始化 MinIO 客户端
    
    #### 5. 爬虫数据获取失败
    
    **问题**：Cookie 失效，无法获取真实数据
    **运行日志**：
    
    ```powershell
    PS C:\Users\31241> python run_crawler.py
    2025-12-15 16:41:27.609|WARNING | app.crawler.xhs_spider:_request_json:74 - Request failed %s status=%s
    2025-12-15 16:41:27.611|INFO | app.crawler.xhs_spider:fetch_notes_by_keyword:118 - keyword=%s fetched=%d
    关键词:美食 返回条数:0
    PS C:\Users\31241\xiaohongshu_spider>
    ```
