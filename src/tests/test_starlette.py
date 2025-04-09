# type: ignore
from starlette.responses import HTMLResponse
from starlette.testclient import TestClient

from markupy import tag


async def starlette_app(scope, receive, send):
    assert scope["type"] == "http"
    response = HTMLResponse(tag.H1(".title")["starlette"])
    await response(scope, receive, send)


def test_starlette() -> None:
    client = TestClient(starlette_app)
    response = client.get("/")
    assert response.text == """<h1 class="title">starlette</h1>"""
