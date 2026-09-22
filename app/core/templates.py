from pathlib import Path

from starlette.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 模板
templates = Jinja2Templates(directory=BASE_DIR / "templates")
