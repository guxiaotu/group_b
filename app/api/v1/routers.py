from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.core.templates import get_template
from app.service.data_mining import get_data

router = APIRouter()


@router.get("/x", response_class=HTMLResponse)
async def hello(
    request: Request,
    templates: Jinja2Templates = Depends(dependency=get_template),
):
    months, counts, ratios, sample_count= get_data()

    return templates.TemplateResponse(
        request=request,
        name="x.jinjia2",
        context={
            "months": months,
            "counts": counts,
            "ratios": ratios,
            "sample_count": sample_count,
        },
    )
