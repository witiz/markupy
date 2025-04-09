import typing

from django.template import Context, Engine  # type:ignore
from jinja2 import Template
from starlette.responses import HTMLResponse
from starlette.testclient import TestClient

from markupy import tag


def test_starlette() -> None:
    @typing.no_type_check
    async def starlette_app(scope, receive, send):
        assert scope["type"] == "http"
        response = HTMLResponse(tag.H1(".title")["starlette"])
        await response(scope, receive, send)

    client = TestClient(starlette_app)  # type: ignore
    response = client.get("/")
    assert response.text == """<h1 class="title">starlette</h1>"""


@typing.no_type_check
def test_django() -> None:
    template_string = "<div>{{ content }}</div>"
    template = Engine().from_string(template_string)
    context = Context({"content": tag.H1(".title")["django"]})
    rendered = template.render(context)
    assert rendered == """<div><h1 class="title">django</h1></div>"""


def test_jinja2() -> None:
    template_string = "<div>{{ content }}</div>"
    template = Template(template_string)
    rendered = template.render(content=tag.H1(".title")["jinja"])
    assert rendered == """<div><h1 class="title">jinja</h1></div>"""
