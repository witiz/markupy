import typing

from django.template import Context, Engine  # type:ignore
from jinja2 import Environment

from markupy import elements


@typing.no_type_check
def test_django() -> None:
    template = Engine().from_string("<div>{{ content }}</div>")
    context = Context({"content": elements.H1(".title")["django"]})
    rendered = template.render(context)
    assert rendered == """<div><h1 class="title">django</h1></div>"""


def test_jinja2() -> None:
    env = Environment(autoescape=True)
    template = env.from_string("<div>{{ content }}</div>")
    rendered = template.render(content=elements.H1(".title")["jinja"])
    assert rendered == """<div><h1 class="title">jinja</h1></div>"""
