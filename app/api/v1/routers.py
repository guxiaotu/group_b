from pathlib import Path

from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# 模板
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@router.get("/query", response_class=HTMLResponse)
async def history(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="x.jinjia2",
        # context={"x": x_view.get_view().model_dump()},
        context={
            "title": "手机壳行业分析大屏",
            "total_sales": 125811,
            "total_reviews": 104563,
            "brands": ["Spigen", "Caseology", "OtterBox", "UAG", "Apple", "Anker"],
            "brand_sales": [32000, 28000, 21000, 18000, 15000, 11811],
            "months": ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"],
            "sales_trend": [8000, 12000, 15000, 14000, 21000, 26000],
            "price_dist": [
                {"value": 35, "name": "0-10"},
                {"value": 45, "name": "10-20"},
                {"value": 60, "name": "20-30"},
                {"value": 30, "name": "30-50"},
                {"value": 12, "name": "50+"},
            ],
            "map_points": [
                {"name": "广东", "value": 9000},
                {"name": "浙江", "value": 6000},
                {"name": "江苏", "value": 5000},
                {"name": "上海", "value": 3000},
                {"name": "北京", "value": 2500},
            ],
        }
    )
