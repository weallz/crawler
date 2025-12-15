-- ============================================
-- 小红书爬虫项目数据库表结构
-- MySQL 8.1+ 版本
-- ============================================

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS xiaohongshu_spider 
    DEFAULT CHARACTER SET utf8mb4 
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE xiaohongshu_spider;

-- ============================================
-- 1. 关键词表 (keywords)
-- ============================================
CREATE TABLE IF NOT EXISTS keywords (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    keyword VARCHAR(255) NOT NULL COMMENT '关键词',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态：1-待爬取，2-爬取中，3-已完成，4-已失败',
    priority INT NOT NULL DEFAULT 0 COMMENT '优先级：数字越大优先级越高',
    total_notes INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '已爬取笔记总数',
    last_crawl_time DATETIME NULL COMMENT '最后爬取时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    UNIQUE KEY uk_keyword (keyword),
    KEY idx_status (status),
    KEY idx_priority (priority),
    KEY idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='关键词表';

-- ============================================
-- 2. 笔记表 (notes)
-- ============================================
CREATE TABLE IF NOT EXISTS notes (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    keyword_id BIGINT UNSIGNED NOT NULL COMMENT '关联关键词ID',
    note_id VARCHAR(100) NOT NULL COMMENT '小红书笔记ID（唯一标识）',
    title VARCHAR(500) NOT NULL DEFAULT '' COMMENT '笔记标题',
    content TEXT COMMENT '笔记正文内容',
    author_id VARCHAR(100) NOT NULL DEFAULT '' COMMENT '作者ID',
    author_name VARCHAR(255) NOT NULL DEFAULT '' COMMENT '作者昵称',
    author_avatar_url VARCHAR(500) NULL COMMENT '作者头像URL（MinIO）',
    like_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '点赞数',
    collect_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '收藏数',
    comment_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '评论数',
    share_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '分享数',
    view_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '浏览量',
    cover_image_url VARCHAR(500) NULL COMMENT '封面图片URL（MinIO）',
    image_urls JSON NULL COMMENT '笔记图片URL列表（MinIO，JSON格式）',
    video_url VARCHAR(500) NULL COMMENT '视频URL（MinIO）',
    note_url VARCHAR(500) NOT NULL COMMENT '笔记原始链接',
    publish_time DATETIME NULL COMMENT '发布时间',
    crawl_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    UNIQUE KEY uk_note_id (note_id),
    KEY idx_keyword_id (keyword_id),
    KEY idx_author_id (author_id),
    KEY idx_like_count (like_count),
    KEY idx_publish_time (publish_time),
    KEY idx_crawl_time (crawl_time),
    CONSTRAINT fk_notes_keyword FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='笔记表';

-- ============================================
-- 3. 评论表 (comments)
-- ============================================
CREATE TABLE IF NOT EXISTS comments (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    note_id BIGINT UNSIGNED NOT NULL COMMENT '关联笔记ID（关联notes表）',
    comment_id VARCHAR(100) NOT NULL COMMENT '评论ID（小红书唯一标识）',
    parent_comment_id VARCHAR(100) NULL COMMENT '父评论ID（用于回复评论）',
    user_id VARCHAR(100) NOT NULL DEFAULT '' COMMENT '评论用户ID',
    user_name VARCHAR(255) NOT NULL DEFAULT '' COMMENT '评论用户昵称',
    user_avatar_url VARCHAR(500) NULL COMMENT '评论用户头像URL（MinIO）',
    content TEXT NOT NULL COMMENT '评论内容',
    like_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '评论点赞数',
    reply_count INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '回复数',
    comment_time DATETIME NULL COMMENT '评论时间',
    crawl_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    UNIQUE KEY uk_comment_id (comment_id),
    KEY idx_note_id (note_id),
    KEY idx_parent_comment_id (parent_comment_id),
    KEY idx_user_id (user_id),
    KEY idx_comment_time (comment_time),
    CONSTRAINT fk_comments_note FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评论表';

-- ============================================
-- 索引优化说明
-- ============================================
-- 1. keywords表：按状态、优先级、创建时间建立索引，便于查询待爬取任务
-- 2. notes表：按关键词ID、作者ID、点赞数、发布时间建立索引，便于数据查询和排序
-- 3. comments表：按笔记ID、父评论ID、用户ID、评论时间建立索引，便于关联查询

