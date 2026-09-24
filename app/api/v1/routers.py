from pathlib import Path

from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.view import x_view

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# 模板
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@router.get("/query", response_class=HTMLResponse)
async def history(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="x.jinjia2",
        context={"x": x_view.get_view().model_dump()},
    )
