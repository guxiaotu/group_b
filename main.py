from pathlib import Path

from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles

from app.api.routers import router as api_router

app = FastAPI(title="ECharts Dashboard")

BASE_DIR = Path(__file__).resolve().parent

# 全局挂载静态文件
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# 注册路由
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root(request: Request):
    return "Hello FastAPI"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", reload=True)
