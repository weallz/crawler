"""
CRUD操作模块
提供关键词、笔记、评论的异步增删改查操作
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from decimal import Decimal

from sqlalchemy import select, update, delete, func, and_, or_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from loguru import logger

from app.db.models import Keyword, Note, Comment


# ============================================
# 关键词CRUD操作
# ============================================

class KeywordCRUD:
    """关键词CRUD操作类"""
    
    @staticmethod
    async def create(
        session: AsyncSession,
        keyword: str,
        status: int = 1,
        priority: int = 0
    ) -> Keyword:
        """
        创建新关键词
        
        Args:
            session: 数据库会话
            keyword: 关键词
            status: 状态（1-待爬取，2-爬取中，3-已完成，4-已失败）
            priority: 优先级
            
        Returns:
            Keyword: 创建的关键词对象
            
        Raises:
            Exception: 当关键词已存在或创建失败时
        """
        try:
            # 检查关键词是否已存在
            existing = await KeywordCRUD.get_by_keyword(session, keyword)
            if existing:
                raise ValueError(f"关键词 '{keyword}' 已存在")
            
            new_keyword = Keyword(
                keyword=keyword,
                status=status,
                priority=priority
            )
            session.add(new_keyword)
            await session.flush()
            await session.refresh(new_keyword)
            
            logger.info(f"创建关键词成功: {keyword} (ID: {new_keyword.id})")
            return new_keyword
        except Exception as e:
            logger.error(f"创建关键词失败: {keyword}, 错误: {e}")
            raise
    
    @staticmethod
    async def get_by_id(session: AsyncSession, keyword_id: int) -> Optional[Keyword]:
        """
        根据ID获取关键词
        
        Args:
            session: 数据库会话
            keyword_id: 关键词ID
            
        Returns:
            Optional[Keyword]: 关键词对象，不存在返回None
        """
        try:
            result = await session.execute(
                select(Keyword).where(Keyword.id == keyword_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"获取关键词失败: ID={keyword_id}, 错误: {e}")
            return None
    
    @staticmethod
    async def get_by_keyword(
        session: AsyncSession,
        keyword: str
    ) -> Optional[Keyword]:
        """
        根据关键词获取对象
        
        Args:
            session: 数据库会话
            keyword: 关键词
            
        Returns:
            Optional[Keyword]: 关键词对象，不存在返回None
        """
        try:
            result = await session.execute(
                select(Keyword).where(Keyword.keyword == keyword)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"获取关键词失败: keyword={keyword}, 错误: {e}")
            return None
    
    @staticmethod
    async def get_all(
        session: AsyncSession,
        status: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "created_at"
    ) -> List[Keyword]:
        """
        获取关键词列表
        
        Args:
            session: 数据库会话
            status: 状态筛选（可选）
            limit: 返回数量限制
            offset: 偏移量
            order_by: 排序字段（created_at, priority, total_notes）
            
        Returns:
            List[Keyword]: 关键词列表
        """
        try:
            query = select(Keyword)
            
            if status is not None:
                query = query.where(Keyword.status == status)
            
            # 排序
            if order_by == "priority":
                query = query.order_by(desc(Keyword.priority), desc(Keyword.created_at))
            elif order_by == "total_notes":
                query = query.order_by(desc(Keyword.total_notes), desc(Keyword.created_at))
            else:
                query = query.order_by(desc(Keyword.created_at))
            
            query = query.limit(limit).offset(offset)
            
            result = await session.execute(query)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"获取关键词列表失败: 错误: {e}")
            return []
    
    @staticmethod
    async def update(
        session: AsyncSession,
        keyword_id: int,
        **kwargs
    ) -> Optional[Keyword]:
        """
        更新关键词
        
        Args:
            session: 数据库会话
            keyword_id: 关键词ID
            **kwargs: 要更新的字段（status, priority, total_notes, last_crawl_time等）
            
        Returns:
            Optional[Keyword]: 更新后的关键词对象，不存在返回None
        """
        try:
            keyword = await KeywordCRUD.get_by_id(session, keyword_id)
            if not keyword:
                return None
            
            for key, value in kwargs.items():
                if hasattr(keyword, key):
                    setattr(keyword, key, value)
            
            await session.flush()
            await session.refresh(keyword)
            
            logger.info(f"更新关键词成功: ID={keyword_id}")
            return keyword
        except Exception as e:
            logger.error(f"更新关键词失败: ID={keyword_id}, 错误: {e}")
            raise
    
    @staticmethod
    async def delete(session: AsyncSession, keyword_id: int) -> bool:
        """
        删除关键词
        
        Args:
            session: 数据库会话
            keyword_id: 关键词ID
            
        Returns:
            bool: 删除是否成功
        """
        try:
            keyword = await KeywordCRUD.get_by_id(session, keyword_id)
            if not keyword:
                return False
            
            await session.delete(keyword)
            await session.flush()
            
            logger.info(f"删除关键词成功: ID={keyword_id}")
            return True
        except Exception as e:
            logger.error(f"删除关键词失败: ID={keyword_id}, 错误: {e}")
            raise
    
    @staticmethod
    async def get_pending_keywords(
        session: AsyncSession,
        limit: int = 10
    ) -> List[Keyword]:
        """
        获取待爬取的关键词（按优先级排序）
        
        Args:
            session: 数据库会话
            limit: 返回数量限制
            
        Returns:
            List[Keyword]: 待爬取的关键词列表
        """
        return await KeywordCRUD.get_all(
            session,
            status=1,
            limit=limit,
            order_by="priority"
        )


# ============================================
# 笔记CRUD操作
# ============================================

class NoteCRUD:
    """笔记CRUD操作类"""
    
    @staticmethod
    async def create(
        session: AsyncSession,
        keyword_id: int,
        note_id: str,
        title: str = "",
        content: Optional[str] = None,
        author_id: str = "",
        author_name: str = "",
        author_avatar_url: Optional[str] = None,
        like_count: int = 0,
        collect_count: int = 0,
        comment_count: int = 0,
        share_count: int = 0,
        view_count: int = 0,
        cover_image_url: Optional[str] = None,
        image_urls: Optional[List[str]] = None,
        video_url: Optional[str] = None,
        note_url: str = "",
        publish_time: Optional[datetime] = None,
        **kwargs
    ) -> Note:
        """
        创建新笔记
        
        Args:
            session: 数据库会话
            keyword_id: 关联关键词ID
            note_id: 小红书笔记ID
            其他参数: 笔记相关字段
            
        Returns:
            Note: 创建的笔记对象
            
        Raises:
            Exception: 当笔记已存在或创建失败时
        """
        try:
            # 检查笔记是否已存在
            existing = await NoteCRUD.get_by_note_id(session, note_id)
            if existing:
                raise ValueError(f"笔记 '{note_id}' 已存在")
            
            new_note = Note(
                keyword_id=keyword_id,
                note_id=note_id,
                title=title,
                content=content,
                author_id=author_id,
                author_name=author_name,
                author_avatar_url=author_avatar_url,
                like_count=like_count,
                collect_count=collect_count,
                comment_count=comment_count,
                share_count=share_count,
                view_count=view_count,
                cover_image_url=cover_image_url,
                image_urls=image_urls,
                video_url=video_url,
                note_url=note_url,
                publish_time=publish_time,
                **kwargs
            )
            session.add(new_note)
            await session.flush()
            await session.refresh(new_note)
            
            # 更新关键词的笔记总数
            await session.execute(
                update(Keyword)
                .where(Keyword.id == keyword_id)
                .values(total_notes=Keyword.total_notes + 1)
            )
            
            logger.info(f"创建笔记成功: {note_id} (ID: {new_note.id})")
            return new_note
        except Exception as e:
            logger.error(f"创建笔记失败: {note_id}, 错误: {e}")
            raise
    
    @staticmethod
    async def batch_create(
        session: AsyncSession,
        notes_data: List[Dict[str, Any]]
    ) -> List[Note]:
        """
        批量创建笔记
        
        Args:
            session: 数据库会话
            notes_data: 笔记数据列表
            
        Returns:
            List[Note]: 创建的笔记对象列表
        """
        created_notes = []
        for note_data in notes_data:
            try:
                note = await NoteCRUD.create(session, **note_data)
                created_notes.append(note)
            except ValueError as e:
                # 笔记已存在，跳过
                logger.warning(f"跳过已存在的笔记: {e}")
                continue
            except Exception as e:
                logger.error(f"批量创建笔记失败: {e}")
                continue
        
        await session.flush()
        logger.info(f"批量创建笔记完成: 成功{len(created_notes)}条")
        return created_notes
    
    @staticmethod
    async def get_by_id(session: AsyncSession, note_id: int) -> Optional[Note]:
        """
        根据ID获取笔记
        
        Args:
            session: 数据库会话
            note_id: 笔记ID
            
        Returns:
            Optional[Note]: 笔记对象，不存在返回None
        """
        try:
            result = await session.execute(
                select(Note)
                .options(selectinload(Note.keyword_obj))
                .where(Note.id == note_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"获取笔记失败: ID={note_id}, 错误: {e}")
            return None
    
    @staticmethod
    async def get_by_note_id(
        session: AsyncSession,
        note_id: str
    ) -> Optional[Note]:
        """
        根据小红书笔记ID获取对象
        
        Args:
            session: 数据库会话
            note_id: 小红书笔记ID
            
        Returns:
            Optional[Note]: 笔记对象，不存在返回None
        """
        try:
            result = await session.execute(
                select(Note).where(Note.note_id == note_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"获取笔记失败: note_id={note_id}, 错误: {e}")
            return None
    
    @staticmethod
    async def get_by_keyword_id(
        session: AsyncSession,
        keyword_id: int,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "crawl_time"
    ) -> List[Note]:
        """
        根据关键词ID获取笔记列表
        
        Args:
            session: 数据库会话
            keyword_id: 关键词ID
            limit: 返回数量限制
            offset: 偏移量
            order_by: 排序字段（crawl_time, like_count, publish_time）
            
        Returns:
            List[Note]: 笔记列表
        """
        try:
            query = select(Note).where(Note.keyword_id == keyword_id)
            
            # 排序
            if order_by == "like_count":
                query = query.order_by(desc(Note.like_count), desc(Note.crawl_time))
            elif order_by == "publish_time":
                query = query.order_by(desc(Note.publish_time))
            else:
                query = query.order_by(desc(Note.crawl_time))
            
            query = query.limit(limit).offset(offset)
            
            result = await session.execute(query)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"获取笔记列表失败: keyword_id={keyword_id}, 错误: {e}")
            return []
    
    @staticmethod
    async def search(
        session: AsyncSession,
        keyword_id: Optional[int] = None,
        author_id: Optional[str] = None,
        min_like_count: Optional[int] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Note]:
        """
        搜索笔记
        
        Args:
            session: 数据库会话
            keyword_id: 关键词ID筛选（可选）
            author_id: 作者ID筛选（可选）
            min_like_count: 最小点赞数筛选（可选）
            limit: 返回数量限制
            offset: 偏移量
            
        Returns:
            List[Note]: 笔记列表
        """
        try:
            query = select(Note)
            conditions = []
            
            if keyword_id:
                conditions.append(Note.keyword_id == keyword_id)
            if author_id:
                conditions.append(Note.author_id == author_id)
            if min_like_count is not None:
                conditions.append(Note.like_count >= min_like_count)
            
            if conditions:
                query = query.where(and_(*conditions))
            
            query = query.order_by(desc(Note.like_count), desc(Note.crawl_time))
            query = query.limit(limit).offset(offset)
            
            result = await session.execute(query)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"搜索笔记失败: 错误: {e}")
            return []
    
    @staticmethod
    async def update(
        session: AsyncSession,
        note_id: int,
        **kwargs
    ) -> Optional[Note]:
        """
        更新笔记
        
        Args:
            session: 数据库会话
            note_id: 笔记ID
            **kwargs: 要更新的字段
            
        Returns:
            Optional[Note]: 更新后的笔记对象，不存在返回None
        """
        try:
            note = await NoteCRUD.get_by_id(session, note_id)
            if not note:
                return None
            
            for key, value in kwargs.items():
                if hasattr(note, key):
                    setattr(note, key, value)
            
            await session.flush()
            await session.refresh(note)
            
            logger.info(f"更新笔记成功: ID={note_id}")
            return note
        except Exception as e:
            logger.error(f"更新笔记失败: ID={note_id}, 错误: {e}")
            raise
    
    @staticmethod
    async def delete(session: AsyncSession, note_id: int) -> bool:
        """
        删除笔记
        
        Args:
            session: 数据库会话
            note_id: 笔记ID
            
        Returns:
            bool: 删除是否成功
        """
        try:
            note = await NoteCRUD.get_by_id(session, note_id)
            if not note:
                return False
            
            keyword_id = note.keyword_id
            await session.delete(note)
            await session.flush()
            
            # 更新关键词的笔记总数
            await session.execute(
                update(Keyword)
                .where(Keyword.id == keyword_id)
                .values(total_notes=func.greatest(Keyword.total_notes - 1, 0))
            )
            
            logger.info(f"删除笔记成功: ID={note_id}")
            return True
        except Exception as e:
            logger.error(f"删除笔记失败: ID={note_id}, 错误: {e}")
            raise


# ============================================
# 评论CRUD操作
# ============================================

class CommentCRUD:
    """评论CRUD操作类"""
    
    @staticmethod
    async def create(
        session: AsyncSession,
        note_id: int,
        comment_id: str,
        content: str,
        user_id: str = "",
        user_name: str = "",
        user_avatar_url: Optional[str] = None,
        parent_comment_id: Optional[str] = None,
        like_count: int = 0,
        reply_count: int = 0,
        comment_time: Optional[datetime] = None,
        **kwargs
    ) -> Comment:
        """
        创建新评论
        
        Args:
            session: 数据库会话
            note_id: 关联笔记ID
            comment_id: 评论ID
            content: 评论内容
            其他参数: 评论相关字段
            
        Returns:
            Comment: 创建的评论对象
            
        Raises:
            Exception: 当评论已存在或创建失败时
        """
        try:
            # 检查评论是否已存在
            existing = await CommentCRUD.get_by_comment_id(session, comment_id)
            if existing:
                raise ValueError(f"评论 '{comment_id}' 已存在")
            
            new_comment = Comment(
                note_id=note_id,
                comment_id=comment_id,
                content=content,
                user_id=user_id,
                user_name=user_name,
                user_avatar_url=user_avatar_url,
                parent_comment_id=parent_comment_id,
                like_count=like_count,
                reply_count=reply_count,
                comment_time=comment_time,
                **kwargs
            )
            session.add(new_comment)
            await session.flush()
            await session.refresh(new_comment)
            
            logger.info(f"创建评论成功: {comment_id} (ID: {new_comment.id})")
            return new_comment
        except Exception as e:
            logger.error(f"创建评论失败: {comment_id}, 错误: {e}")
            raise
    
    @staticmethod
    async def batch_create(
        session: AsyncSession,
        comments_data: List[Dict[str, Any]]
    ) -> List[Comment]:
        """
        批量创建评论
        
        Args:
            session: 数据库会话
            comments_data: 评论数据列表
            
        Returns:
            List[Comment]: 创建的评论对象列表
        """
        created_comments = []
        for comment_data in comments_data:
            try:
                comment = await CommentCRUD.create(session, **comment_data)
                created_comments.append(comment)
            except ValueError as e:
                # 评论已存在，跳过
                logger.warning(f"跳过已存在的评论: {e}")
                continue
            except Exception as e:
                logger.error(f"批量创建评论失败: {e}")
                continue
        
        await session.flush()
        logger.info(f"批量创建评论完成: 成功{len(created_comments)}条")
        return created_comments
    
    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        comment_id: int
    ) -> Optional[Comment]:
        """
        根据ID获取评论
        
        Args:
            session: 数据库会话
            comment_id: 评论ID
            
        Returns:
            Optional[Comment]: 评论对象，不存在返回None
        """
        try:
            result = await session.execute(
                select(Comment)
                .options(selectinload(Comment.note_obj))
                .where(Comment.id == comment_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"获取评论失败: ID={comment_id}, 错误: {e}")
            return None
    
    @staticmethod
    async def get_by_comment_id(
        session: AsyncSession,
        comment_id: str
    ) -> Optional[Comment]:
        """
        根据评论ID获取对象
        
        Args:
            session: 数据库会话
            comment_id: 评论ID
            
        Returns:
            Optional[Comment]: 评论对象，不存在返回None
        """
        try:
            result = await session.execute(
                select(Comment).where(Comment.comment_id == comment_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"获取评论失败: comment_id={comment_id}, 错误: {e}")
            return None
    
    @staticmethod
    async def get_by_note_id(
        session: AsyncSession,
        note_id: int,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "comment_time"
    ) -> List[Comment]:
        """
        根据笔记ID获取评论列表
        
        Args:
            session: 数据库会话
            note_id: 笔记ID
            limit: 返回数量限制
            offset: 偏移量
            order_by: 排序字段（comment_time, like_count）
            
        Returns:
            List[Comment]: 评论列表
        """
        try:
            query = select(Comment).where(Comment.note_id == note_id)
            
            # 排序
            if order_by == "like_count":
                query = query.order_by(desc(Comment.like_count), desc(Comment.comment_time))
            else:
                query = query.order_by(desc(Comment.comment_time))
            
            query = query.limit(limit).offset(offset)
            
            result = await session.execute(query)
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"获取评论列表失败: note_id={note_id}, 错误: {e}")
            return []
    
    @staticmethod
    async def get_replies(
        session: AsyncSession,
        parent_comment_id: str,
        limit: int = 50
    ) -> List[Comment]:
        """
        获取评论的回复列表
        
        Args:
            session: 数据库会话
            parent_comment_id: 父评论ID
            limit: 返回数量限制
            
        Returns:
            List[Comment]: 回复列表
        """
        try:
            result = await session.execute(
                select(Comment)
                .where(Comment.parent_comment_id == parent_comment_id)
                .order_by(desc(Comment.comment_time))
                .limit(limit)
            )
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"获取回复列表失败: parent_comment_id={parent_comment_id}, 错误: {e}")
            return []
    
    @staticmethod
    async def update(
        session: AsyncSession,
        comment_id: int,
        **kwargs
    ) -> Optional[Comment]:
        """
        更新评论
        
        Args:
            session: 数据库会话
            comment_id: 评论ID
            **kwargs: 要更新的字段
            
        Returns:
            Optional[Comment]: 更新后的评论对象，不存在返回None
        """
        try:
            comment = await CommentCRUD.get_by_id(session, comment_id)
            if not comment:
                return None
            
            for key, value in kwargs.items():
                if hasattr(comment, key):
                    setattr(comment, key, value)
            
            await session.flush()
            await session.refresh(comment)
            
            logger.info(f"更新评论成功: ID={comment_id}")
            return comment
        except Exception as e:
            logger.error(f"更新评论失败: ID={comment_id}, 错误: {e}")
            raise
    
    @staticmethod
    async def delete(session: AsyncSession, comment_id: int) -> bool:
        """
        删除评论
        
        Args:
            session: 数据库会话
            comment_id: 评论ID
            
        Returns:
            bool: 删除是否成功
        """
        try:
            comment = await CommentCRUD.get_by_id(session, comment_id)
            if not comment:
                return False
            
            await session.delete(comment)
            await session.flush()
            
            logger.info(f"删除评论成功: ID={comment_id}")
            return True
        except Exception as e:
            logger.error(f"删除评论失败: ID={comment_id}, 错误: {e}")
            raise

