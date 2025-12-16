# 数据目录

本目录存放爬取结果数据。

## 目录结构

```
data/
├── README.md          # 本说明文件
└── notes/            # 笔记数据目录
    └── result_note.md # 爬取的笔记数据（Markdown 格式）
    └── bug.md #记录爬虫开发过程中遇到的问题及解决方案（Markdown 格式）

```

## 使用说明

### 笔记数据

将爬取下来的笔记数据 Markdown 文件放在 `notes/` 目录下。

**文件命名建议：**
- `result_note.md` - 通用结果文件
- `notes_YYYYMMDD.md` - 按日期命名
- `notes_keyword.md` - 按关键词命名

### 数据格式

笔记数据建议使用 Markdown 格式存储，便于阅读和处理。

### 注意事项

1. 本目录已被 `.gitignore` 忽略，数据文件不会提交到 Git 仓库
2. 如需版本控制，可以手动将特定文件添加到 Git
3. 建议定期备份重要数据

## 扩展目录（可选）

未来可以根据需要添加以下目录：

- `comments/` - 评论数据
- `images/` - 图片文件
- `videos/` - 视频文件
- `exports/` - 导出数据

