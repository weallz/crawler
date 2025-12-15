"""
FastAPI 路由定义
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.task.async_scheduler import TaskScheduler, get_scheduler


class CrawlTaskRequest(BaseModel):
    keywords: List[str] = Field(..., description="关键词列表", min_length=1)
    note_limit: int = Field(50, gt=0, le=200, description="每个关键词抓取数量")


class ResponseModel(BaseModel):
    code: int = 200
    msg: str = "success"
    data: Optional[dict] = None


router = APIRouter(prefix="/api")


@router.post("/crawl/task", response_model=ResponseModel)
async def create_crawl_task(
    payload: CrawlTaskRequest,
    scheduler: TaskScheduler = Depends(get_scheduler),
):
    created, skipped = await scheduler.enqueue_keywords(payload.keywords, payload.note_limit)
    return ResponseModel(
        data={
            "created": created,
            "skipped": skipped,
        }
    )


@router.get("/crawl/keywords", response_model=ResponseModel)
async def list_keywords(scheduler: TaskScheduler = Depends(get_scheduler)):
    tasks = await scheduler.list_tasks()
    return ResponseModel(data={"tasks": tasks})


@router.get("/crawl/result", response_model=ResponseModel)
async def get_result(
    keyword: str = Query(..., description="关键词"),
    scheduler: TaskScheduler = Depends(get_scheduler),
):
    result = await scheduler.get_result(keyword)
    if result is None:
        raise HTTPException(status_code=404, detail="keyword not found")
    return ResponseModel(data={"keyword": keyword, "notes": result})

