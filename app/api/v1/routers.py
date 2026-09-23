from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.api.views import x_view
from app.core.templates import get_template

router = APIRouter()


@router.get("/x", response_class=HTMLResponse)
async def hello(
    request: Request,
    templates: Jinja2Templates = Depends(dependency=get_template),
):
    return templates.TemplateResponse(
        request=request,
        name="x.jinjia2",
        context={"x": x_view.get_view().model_dump()},
    )
