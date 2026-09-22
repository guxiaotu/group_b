from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

from app.core.templates import templates

router = APIRouter()

@router.get("/hello", response_class=HTMLResponse)
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


@router.get("/data", response_class=HTMLResponse)
async def hello(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="上架月份分布图.html",
    )
