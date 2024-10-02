# Integrating with Starlette

markupy can be used with Starlette to generate HTML. Since FastAPI is built upon Starlette, markupy can also be used with FastAPI.

To return HTML contents, pass a markupy element to Starlette's `HTMLResponse`:

```python
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route

from markupy.tag import H1


async def index(request: Request) -> HTMLResponse:
    return HTMLResponse(H1["Hi Starlette!"])


app = Starlette(routes=[Route("/", index)])
```
