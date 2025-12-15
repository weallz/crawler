"""
异步小红书爬虫核心模块
"""

from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, List, Optional

import aiohttp
from dotenv import load_dotenv
from loguru import logger

from .utils import (
    build_headers,
    dedup_images,
    is_within_last_months,
    parse_publish_time,
    random_delay,
    sanitize_text,
)

# 加载 .env
load_dotenv()


class AsyncXhsCrawler:
    """
    小红书异步爬虫
    """

    def __init__(
        self,
        cookies: Optional[str] = None,
        request_delay: Optional[float] = None,
        comment_limit: Optional[int] = None,
        concurrency: int = 5,
        timeout: float = 15.0,
    ) -> None:
        """
        Args:
            cookies: 可选，传入小红书 Cookie 字符串以提升稳定性
            request_delay: 请求基础延迟秒，默认读取 CRAWLER_DELAY（.env）
            comment_limit: 每条笔记最多抓取评论数，默认读取 COMMENT_LIMIT（.env，默认20）
            concurrency: 并发协程数
            timeout: 单请求超时时间
        """
        self.cookies = cookies or os.getenv("XHS_COOKIES", "")
        self.request_delay = (
            float(request_delay)
            if request_delay is not None
            else float(os.getenv("CRAWLER_DELAY", "1"))
        )
        self.comment_limit = (
            int(comment_limit)
            if comment_limit is not None
            else int(os.getenv("COMMENT_LIMIT", "20"))
        )
        self.concurrency = concurrency
        self.timeout = timeout
        self.sem = asyncio.Semaphore(concurrency)

    async def _request_json(self, session: aiohttp.ClientSession, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        headers = build_headers()
        if self.cookies:
            headers["Cookie"] = self.cookies

        async with self.sem:
            await asyncio.sleep(random_delay(self.request_delay))
            try:
                async with session.get(url, params=params, headers=headers, timeout=self.timeout) as resp:
                    if resp.status != 200:
                        logger.warning("Request failed %s status=%s", url, resp.status)
                        return {}
                    return await resp.json()
            except asyncio.TimeoutError:
                logger.error("Request timeout %s", url)
            except aiohttp.ClientError as exc:
                logger.error("Request error %s: %s", url, exc)
        return {}

    async def fetch_notes_by_keyword(
        self,
        session: aiohttp.ClientSession,
        keyword: str,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        通过关键词搜索笔记（示例接口占位）
        """
        notes: List[Dict[str, Any]] = []
        page = 1
        page_size = 20
        base_url = "https://www.xiaohongshu.com/api/fe_api/burdock/v3/search/notes"

        while len(notes) < limit:
            params = {"keyword": keyword, "page": page, "page_size": page_size}
            data = await self._request_json(session, base_url, params)
            items = data.get("data", {}).get("notes", []) if data else []
            if not items:
                break
            for item in items:
                parsed = self.extract_note_data(item)
                if not parsed:
                    continue
                if parsed.get("note_type") != "normal":  # 过滤视频/广告
                    continue
                if not is_within_last_months(parsed.get("publish_time"), months=6):
                    continue
                notes.append(parsed)
                if len(notes) >= limit:
                    break
            page += 1

        # 只保留评论量最高的 limit 条图文笔记
        notes = sorted(notes, key=lambda n: n.get("commented", 0), reverse=True)[:limit]
        logger.info("keyword=%s fetched=%d", keyword, len(notes))
        return notes

    def extract_note_data(self, item: Dict[str, Any]) -> Dict[str, Any] | None:
        """
        解析单条笔记数据
        """
        if not item:
            return None
        note_id = item.get("id") or item.get("note_id")
        if not note_id:
            return None
        title = sanitize_text(item.get("title", ""))
        desc = sanitize_text(item.get("desc", ""))
        liked = item.get("liked_count") or item.get("like_count") or 0
        collected = item.get("collected_count") or item.get("fav_count") or 0
        commented = item.get("comment_count") or 0
        ts = item.get("time") or item.get("publish_time") or item.get("create_time") or ""
        publish_time = parse_publish_time(ts)
        images = dedup_images(item.get("image_list", []) or item.get("images", []))
        note_type = item.get("type") or item.get("note_type") or "normal"

        return {
            "note_id": note_id,
            "title": title,
            "desc": desc,
            "liked": liked,
            "collected": collected,
            "commented": commented,
            "publish_time": publish_time,
            "images": images,
            "note_type": note_type,
        }

    async def fetch_comments(
        self,
        session: aiohttp.ClientSession,
        note_id: str,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        拉取评论（示例接口占位），默认前 N 条
        """
        max_comments = limit or self.comment_limit
        base_url = "https://www.xiaohongshu.com/api/sns/web/v2/comment/page"
        comments: List[Dict[str, Any]] = []
        cursor = ""

        while len(comments) < max_comments:
            params = {"note_id": note_id, "cursor": cursor, "page_size": 20}
            data = await self._request_json(session, base_url, params)
            items = data.get("data", {}).get("comments", []) if data else []
            if not items:
                break
            for c in items:
                content = sanitize_text(c.get("content", ""))
                if content:
                    comments.append(
                        {
                            "user": c.get("user_info", {}).get("nickname", ""),
                            "content": content,
                            "liked": c.get("like_count", 0),
                        }
                    )
                if len(comments) >= max_comments:
                    break
            cursor = data.get("data", {}).get("cursor", "")
            if not cursor:
                break

        return comments

    async def crawl_keywords(
        self,
        keywords: List[str],
        per_keyword: int = 50,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        批量关键词爬取
        """
        results: Dict[str, List[Dict[str, Any]]] = {}

        timeout = aiohttp.ClientTimeout(total=None, sock_connect=self.timeout, sock_read=self.timeout)
        connector = aiohttp.TCPConnector(limit=50, ssl=False)
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            for kw in keywords:
                notes = await self.fetch_notes_by_keyword(session, kw, limit=per_keyword)
                # 拉取评论
                for note in notes:
                    note_id = note.get("note_id")
                    if not note_id:
                        continue
                    try:
                        comments = await self.fetch_comments(session, note_id)
                        note["comments"] = comments[:20]
                    except Exception as exc:
                        logger.error("fetch_comments failed note_id=%s err=%s", note_id, exc)
                        note["comments"] = []
                results[kw] = notes
        return results


__all__ = ["AsyncXhsCrawler"]

