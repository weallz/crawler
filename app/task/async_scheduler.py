"""
异步任务调度：生产者-消费者（数据库轮询的模拟实现）

当前实现使用内存存储模拟数据库，便于快速落地。
如需真正落地到数据库，可将 InMemoryStore 替换为数据库 CRUD。
"""

from __future__ import annotations

import asyncio
import os
from typing import Dict, List, Optional, Tuple

from loguru import logger

from app.crawler import AsyncXhsCrawler


class InMemoryStore:
    """
    内存模拟数据库。
    task 状态: pending / running / success / failed
    """

    def __init__(self) -> None:
        self._tasks: Dict[str, dict] = {}
        self._results: Dict[str, list] = {}
        self._lock = asyncio.Lock()

    async def add_tasks(self, keywords: List[str], note_limit: int) -> Tuple[List[str], List[str]]:
        """
        添加任务，返回(新建, 已存在)
        """
        created, skipped = [], []
        async with self._lock:
            for kw in keywords:
                if kw in self._tasks and self._tasks[kw]["status"] in {"pending", "running"}:
                    skipped.append(kw)
                    continue
                self._tasks[kw] = {"keyword": kw, "status": "pending", "note_limit": note_limit, "error": None}
                created.append(kw)
        return created, skipped

    async def list_tasks(self) -> List[dict]:
        async with self._lock:
            return list(self._tasks.values())

    async def get_pending(self, limit: int) -> List[dict]:
        async with self._lock:
            pending = [t for t in self._tasks.values() if t["status"] == "pending"]
            return pending[:limit]

    async def mark_running(self, keyword: str) -> None:
        async with self._lock:
            if keyword in self._tasks:
                self._tasks[keyword]["status"] = "running"

    async def mark_done(self, keyword: str, notes: list) -> None:
        async with self._lock:
            if keyword in self._tasks:
                self._tasks[keyword]["status"] = "success"
                self._results[keyword] = notes

    async def mark_failed(self, keyword: str, error: str) -> None:
        async with self._lock:
            if keyword in self._tasks:
                self._tasks[keyword]["status"] = "failed"
                self._tasks[keyword]["error"] = error

    async def get_result(self, keyword: str) -> Optional[list]:
        async with self._lock:
            return self._results.get(keyword)


class TaskScheduler:
    """
    简单的轮询调度器，基于 asyncio 协程并发执行，不依赖消息队列。
    """

    def __init__(self, store: InMemoryStore, concurrency: int = 3, poll_interval: float = 2.0) -> None:
        self.store = store
        self.concurrency = concurrency
        self.poll_interval = poll_interval
        self._stop_event = asyncio.Event()
        self._worker_task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        if self._worker_task is None or self._worker_task.done():
            self._worker_task = asyncio.create_task(self._worker_loop())
            logger.info("TaskScheduler started with concurrency=%s", self.concurrency)

    async def shutdown(self) -> None:
        self._stop_event.set()
        if self._worker_task:
            await self._worker_task

    async def enqueue_keywords(self, keywords: List[str], note_limit: int) -> Tuple[List[str], List[str]]:
        return await self.store.add_tasks(keywords, note_limit)

    async def list_tasks(self) -> List[dict]:
        return await self.store.list_tasks()

    async def get_result(self, keyword: str) -> Optional[list]:
        return await self.store.get_result(keyword)

    async def _worker_loop(self) -> None:
        sem = asyncio.Semaphore(self.concurrency)
        while not self._stop_event.is_set():
            pending = await self.store.get_pending(self.concurrency * 2)
            if not pending:
                await asyncio.sleep(self.poll_interval)
                continue

            async def handle(task: dict):
                async with sem:
                    kw = task["keyword"]
                    await self.store.mark_running(kw)
                    try:
                        crawler = AsyncXhsCrawler()
                        notes = await crawler.crawl_keywords([kw], per_keyword=task["note_limit"])
                        await self.store.mark_done(kw, notes.get(kw, []))
                        logger.info("crawl success keyword=%s count=%s", kw, len(notes.get(kw, [])))
                    except Exception as exc:  # pylint: disable=broad-except
                        logger.error("crawl failed keyword=%s err=%s", kw, exc)
                        await self.store.mark_failed(kw, str(exc))

            await asyncio.gather(*(handle(t) for t in pending))
            await asyncio.sleep(self.poll_interval)


_store = InMemoryStore()
_scheduler = TaskScheduler(
    store=_store,
    concurrency=int(os.getenv("SCHEDULER_CONCURRENCY", "3")),
    poll_interval=float(os.getenv("SCHEDULER_POLL_INTERVAL", "2")),
)


async def get_scheduler() -> TaskScheduler:  # FastAPI Depends
    return _scheduler


async def startup_scheduler() -> None:
    await _scheduler.start()


async def shutdown_scheduler() -> None:
    await _scheduler.shutdown()


__all__ = [
    "TaskScheduler",
    "get_scheduler",
    "startup_scheduler",
    "shutdown_scheduler",
]

