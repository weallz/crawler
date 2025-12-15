import os
import asyncio
from dotenv import load_dotenv
from app.crawler import AsyncXhsCrawler


load_dotenv()


async def main():
    # 关键词和数量可按需修改或从环境读取
    keyword = os.getenv("XHS_KEYWORD", "美食")
    per_keyword = int(os.getenv("XHS_PER_KEYWORD", "50"))

    crawler = AsyncXhsCrawler(
        cookies=os.getenv("XHS_COOKIES") or None,  # 如有稳定 Cookie 填在 .env
        request_delay=None,  # 读取 .env CRAWLER_DELAY
        comment_limit=None,  # 读取 .env COMMENT_LIMIT
        concurrency=5,
        timeout=15.0,
    )

    res = await crawler.crawl_keywords([keyword], per_keyword=per_keyword)
    for kw, notes in res.items():
        print("关键词:", kw, "返回条数:", len(notes))
        if notes:
            top = notes[0]
            print(
                "示例第一条:",
                {
                    "note_id": top.get("note_id"),
                    "title": top.get("title"),
                    "commented": top.get("commented"),
                    "publish_time": top.get("publish_time"),
                    "images_cnt": len(top.get("images", [])),
                    "has_comments": bool(top.get("comments")),
                },
            )


if __name__ == "__main__":
    asyncio.run(main())