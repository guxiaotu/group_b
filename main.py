from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

# 挂载静态资源：浏览器访问 /static/xxx
app.mount("/static", StaticFiles(directory=BASE_DIR / "dist/static"), name="static")

# 配置模板目录
templates = Jinja2Templates(directory=BASE_DIR / "dist/templates")


@app.get("/")
async def root(request: Request):
    return "Hello FastAPI"


@app.get("/hello", response_class=HTMLResponse)
async def hello(request: Request):
    sales = [85, 92, 78, 110, 135, 158, 172, 165, 140, 120, 105, 95]
    profit = [22, 28, 20, 35, 48, 62, 75, 68, 52, 40, 32, 25]
    rate = [25.9, 30.4, 25.6, 31.8, 35.6, 39.2, 43.6, 41.2, 37.1, 33.3, 30.5, 26.3]

    return templates.TemplateResponse(
        request=request,
        name="hello.html",
        context={
            "sales": sales,
            "profit": profit,
            "rate": rate,
        },
    )


@app.get("/data", response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="上架月份分布图.html",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", reload=True)
