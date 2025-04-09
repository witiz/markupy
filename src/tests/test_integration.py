import typing

from django.template import Context, Engine  # type:ignore
from jinja2 import Template

from markupy import tag


@typing.no_type_check
def test_django() -> None:
    template_string = "<div>{{ content }}</div>"
    template = Engine().from_string(template_string)
    context = Context({"content": tag.H1(".title")["hello"]})
    rendered = template.render(context)
    assert rendered == """<div><h1 class="title">hello</h1></div>"""


def test_jinja2() -> None:
    template_string = "<div>{{ content }}</div>"
    template = Template(template_string)
    rendered = template.render(content=tag.H1(".title")["hello"])
    assert rendered == """<div><h1 class="title">hello</h1></div>"""
