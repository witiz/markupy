from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route

from markupy.elements import H1, Body, Html


async def index(request: Request) -> HTMLResponse:
    return HTMLResponse(Html[Body[H1["Hi Starlette!"]]])


# Run it with `uv run uvicorn html_response:app``
app = Starlette(
    routes=[Route("/", index)],
)
