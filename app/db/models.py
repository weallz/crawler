"""
数据模型模块
定义关键词、笔记、评论的ORM模型
"""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    JSON,
    ForeignKey,
    Index,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import BIGINT, TINYINT, INTEGER

# #region agent log
import json
from datetime import datetime as dt
try:
    with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix","hypothesisId":"E","location":"models.py:21","message":"Models module importing","data":{"BIGINT_imported":True},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
except: pass
# #endregion

from app.db.conn import Base


class Keyword(Base):
    """
    关键词表模型
    """
    __tablename__ = "keywords"
    
    # 主键
    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
        comment="主键ID"
    )
    
    # 关键词字段
    keyword: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        comment="关键词"
    )
    
    # 状态：1-待爬取，2-爬取中，3-已完成，4-已失败
    status: Mapped[int] = mapped_column(
        TINYINT,
        nullable=False,
        default=1,
        comment="状态：1-待爬取，2-爬取中，3-已完成，4-已失败"
    )
    
    # 优先级
    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="优先级：数字越大优先级越高"
    )
    
    # 已爬取笔记总数
    total_notes: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        nullable=False,
        default=0,
        comment="已爬取笔记总数"
    )
    
    # 最后爬取时间
    last_crawl_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="最后爬取时间"
    )
    
    # 时间戳
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="创建时间"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )
    
    # 关系映射
    notes: Mapped[List["Note"]] = relationship(
        "Note",
        back_populates="keyword_obj",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    # 索引
    __table_args__ = (
        Index("idx_status", "status"),
        Index("idx_priority", "priority"),
        Index("idx_created_at", "created_at"),
    )
    
    def __repr__(self) -> str:
        return f"<Keyword(id={self.id}, keyword='{self.keyword}', status={self.status})>"


class Note(Base):
    """
    笔记表模型
    """
    __tablename__ = "notes"
    
    # 主键
    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
        comment="主键ID"
    )
    
    # 外键：关联关键词ID
    keyword_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("keywords.id", ondelete="CASCADE"),
        nullable=False,
        comment="关联关键词ID"
    )
    
    # 小红书笔记ID（唯一标识）
    note_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        comment="小红书笔记ID（唯一标识）"
    )
    
    # 笔记标题
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        default="",
        comment="笔记标题"
    )
    
    # 笔记正文内容
    content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="笔记正文内容"
    )
    
    # 作者信息
    author_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="",
        comment="作者ID"
    )
    
    author_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="",
        comment="作者昵称"
    )
    
    author_avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="作者头像URL（MinIO）"
    )
    
    # 互动数据
    like_count: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        comment="点赞数"
    )
    
    collect_count: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        comment="收藏数"
    )
    
    comment_count: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        comment="评论数"
    )
    
    share_count: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        comment="分享数"
    )
    
    view_count: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        comment="浏览量"
    )
    
    # 媒体资源
    cover_image_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="封面图片URL（MinIO）"
    )
    
    image_urls: Mapped[Optional[list]] = mapped_column(
        JSON,
        nullable=True,
        comment="笔记图片URL列表（MinIO，JSON格式）"
    )
    
    video_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="视频URL（MinIO）"
    )
    
    # 链接和时间
    note_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="笔记原始链接"
    )
    
    publish_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="发布时间"
    )
    
    crawl_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="爬取时间"
    )
    
    # 时间戳
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="创建时间"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )
    
    # 关系映射
    keyword_obj: Mapped["Keyword"] = relationship(
        "Keyword",
        back_populates="notes",
        lazy="selectin"
    )
    
    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        back_populates="note_obj",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    # 索引
    __table_args__ = (
        Index("idx_keyword_id", "keyword_id"),
        Index("idx_author_id", "author_id"),
        Index("idx_like_count", "like_count"),
        Index("idx_publish_time", "publish_time"),
        Index("idx_crawl_time", "crawl_time"),
    )
    
    def __repr__(self) -> str:
        # #region agent log
        try:
            with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix","hypothesisId":"F","location":"models.py:308","message":"Note class defined successfully","data":{},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
        except: pass
        # #endregion
        return f"<Note(id={self.id}, note_id='{self.note_id}', title='{self.title[:30]}...')>"


class Comment(Base):
    """
    评论表模型
    """
    __tablename__ = "comments"
    
    # 主键
    id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
        comment="主键ID"
    )
    
    # 外键：关联笔记ID
    note_id: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("notes.id", ondelete="CASCADE"),
        nullable=False,
        comment="关联笔记ID（关联notes表）"
    )
    
    # 评论ID（小红书唯一标识）
    comment_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        comment="评论ID（小红书唯一标识）"
    )
    
    # 父评论ID（用于回复评论）
    parent_comment_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="父评论ID（用于回复评论）"
    )
    
    # 用户信息
    user_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="",
        comment="评论用户ID"
    )
    
    user_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="",
        comment="评论用户昵称"
    )
    
    user_avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="评论用户头像URL（MinIO）"
    )
    
    # 评论内容
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="评论内容"
    )
    
    # 互动数据
    like_count: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        comment="评论点赞数"
    )
    
    reply_count: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        nullable=False,
        default=0,
        comment="回复数"
    )
    
    # 时间
    comment_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="评论时间"
    )
    
    crawl_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="爬取时间"
    )
    
    # 时间戳
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="创建时间"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )
    
    # 关系映射
    note_obj: Mapped["Note"] = relationship(
        "Note",
        back_populates="comments",
        lazy="selectin"
    )
    
    # 索引
    __table_args__ = (
        Index("idx_note_id", "note_id"),
        Index("idx_parent_comment_id", "parent_comment_id"),
        Index("idx_user_id", "user_id"),
        Index("idx_comment_time", "comment_time"),
    )
    
    def __repr__(self) -> str:
        # #region agent log
        try:
            with open(r'c:\Users\31241\xiaohongshu_spider\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix","hypothesisId":"F","location":"models.py:437","message":"Comment class defined successfully","data":{},"timestamp":int(dt.now().timestamp()*1000)})+'\n')
        except: pass
        # #endregion
        return f"<Comment(id={self.id}, comment_id='{self.comment_id}', content='{self.content[:30]}...')>"

