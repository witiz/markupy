# type: ignore
from starlette.responses import HTMLResponse, StreamingResponse
from starlette.testclient import TestClient

from markupy import elements


async def render(scope, receive, send):
    assert scope["type"] == "http"
    response = HTMLResponse(elements.H1(".title")["render"])
    await response(scope, receive, send)


async def stream(scope, receive, send):
    assert scope["type"] == "http"
    response = StreamingResponse(iter(elements.H1(".title")["stream"]))
    await response(scope, receive, send)


def test_render() -> None:
    client = TestClient(render)
    response = client.get("/")
    assert response.text == """<h1 class="title">render</h1>"""


def test_stream() -> None:
    client = TestClient(stream)
    response = client.get("/")
    assert response.text == """<h1 class="title">stream</h1>"""
