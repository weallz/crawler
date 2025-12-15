import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from starlette.staticfiles import StaticFiles
from dotenv import load_dotenv
from loguru import logger

from app.api.router import router
from app.task.async_scheduler import startup_scheduler, shutdown_scheduler

try:
    # 本地 swagger 资源，避免外网 CDN 失败
    from swagger_ui_bundle import swagger_ui_path  # type: ignore
except ImportError:
    swagger_ui_path = None

load_dotenv()

app = FastAPI(
    title="小红书爬虫API",
    description="基于FastAPI+异步IO的小红书爬虫项目",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请限制来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

# 本地化 swagger 资源，避免 CDN 加载失败
if swagger_ui_path:
    app.mount("/_swagger", StaticFiles(directory=swagger_ui_path), name="swagger-ui")

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} - Docs",
            swagger_js_url="/_swagger/swagger-ui-bundle.js",
            swagger_css_url="/_swagger/swagger-ui.css",
            swagger_favicon_url="/_swagger/favicon-32x32.png",
        )

    @app.get("/docs/oauth2-redirect", include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()


@app.on_event("startup")
async def _startup() -> None:
    await startup_scheduler()
    logger.info("scheduler started")


@app.on_event("shutdown")
async def _shutdown() -> None:
    await shutdown_scheduler()
    logger.info("scheduler stopped")


@app.get("/")
async def root():
    return {"message": "小红书爬虫API服务", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


def main():
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
