from dataclasses import dataclass, field

import pytest

from markupy import Component, Fragment, View, tag
from markupy.exception import MarkupyError


class ComponentElement(Component):
    def __init__(self, id: str):
        self.id = id

    def render(self) -> View:
        return tag.Div(id=self.id)


def test_component_element() -> None:
    assert str(ComponentElement("component")) == """<div id="component"></div>"""


class ComponentFragment(Component):
    def render(self) -> View:
        return Fragment[tag.Div, tag.Img]


def test_uninitialized_component() -> None:
    with pytest.raises(MarkupyError):
        tag.P[ComponentFragment]


def test_component_fragment() -> None:
    assert str(ComponentFragment()) == """<div></div><img>"""


class ComponentInComponent(Component):
    def render(self) -> View:
        return Fragment[tag.Input, ComponentElement("inside")]


def test_component_in_component() -> None:
    assert str(ComponentInComponent()) == """<input><div id="inside"></div>"""


class ComponentAsComponent(Component):
    def render(self) -> View:
        return ComponentElement("other")


def test_component_as_component() -> None:
    assert str(ComponentAsComponent()) == """<div id="other"></div>"""


class ContentComponent(Component):
    def __init__(self, id: str) -> None:
        super().__init__()
        self.id = id

    def render(self) -> View:
        return tag.H1(".title.header", id=self.id)[self.render_content()]


def test_component_content() -> None:
    assert (
        str(ContentComponent(id="test")["Hello", tag.Div[tag.Input]])
        == """<h1 class="title header" id="test">Hello<div><input></div></h1>"""
    )


def test_component_content_escape() -> None:
    # Make sure component contents are not re-escaped when assigned to element children
    assert (
        str(ContentComponent(id="test")['He>"llo'])
        == """<h1 class="title header" id="test">He&gt;&#34;llo</h1>"""
    )


class TypeErrorComponent(Component):
    def render(self) -> str:  # type:ignore
        return "Hello"


def test_type_error_component() -> None:
    with pytest.raises(MarkupyError):
        str(TypeErrorComponent())


class SuperErrorComponent(Component):
    def __init__(self, *, id: str) -> None:
        # Missing the call to super().__init()
        # calls to __getitem__() will fail
        self.id = id

    def render(self) -> View:
        return tag.H1(id=self.id)


def test_super_error_component() -> None:
    assert str(SuperErrorComponent(id="foo")) == """<h1 id="foo"></h1>"""
    with pytest.raises(MarkupyError):
        SuperErrorComponent(id="foo")["bar"]


@dataclass
class DataComponent(Component):
    href: str = field(default="https://google.com")

    def render(self) -> View:
        return tag.A(href=self.href)[self.render_content()]


def test_dataclass_component() -> None:
    result = """<a href="https://google.com">Google</a>"""
    assert str(DataComponent()["Google"]) == result
