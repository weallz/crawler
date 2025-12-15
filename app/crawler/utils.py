"""
小红书爬虫工具函数
"""

import random
import re
import string
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

USER_AGENTS: List[str] = [
    # 常见桌面 UA，可按需扩充
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
]


def random_user_agent() -> str:
    """返回一个随机 UA"""
    return random.choice(USER_AGENTS)


def build_headers(base: Dict[str, str] | None = None) -> Dict[str, str]:
    """
    构造请求头，自动加入随机 UA
    """
    headers = {
        "User-Agent": random_user_agent(),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
    }
    if base:
        headers.update(base)
    return headers


def sanitize_text(text: str) -> str:
    """
    清洗文案中的特殊字符与多余空白
    """
    if not text:
        return ""
    # 去掉控制字符
    text = re.sub(r"[\x00-\x1f\x7f]", "", text)
    # 归一化空白
    text = " ".join(text.split())
    return text.strip()


def dedup_images(urls: List[str]) -> List[str]:
    """图片 URL 去重，保持顺序"""
    seen = set()
    result = []
    for u in urls:
        if u and u not in seen:
            seen.add(u)
            result.append(u)
    return result


def parse_publish_time(ts: str) -> datetime | None:
    """
    将时间字符串解析为 datetime（假设为 ISO8601 或 RFC3339，回退简单格式）
    """
    if not ts:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            continue
    return None


def is_within_last_months(dt: datetime | None, months: int = 6) -> bool:
    """判断时间是否在最近 N 个月内"""
    if not dt:
        return False
    cutoff = datetime.now(dt.tzinfo) - timedelta(days=30 * months)
    return dt >= cutoff


def random_delay(base_seconds: float = 1.0, jitter: float = 0.3) -> float:
    """
    基于基础延迟和抖动生成延迟秒数
    """
    return max(0.0, random.uniform(base_seconds * (1 - jitter), base_seconds * (1 + jitter)))

