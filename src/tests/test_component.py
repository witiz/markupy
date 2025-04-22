from dataclasses import dataclass, field

import pytest

from markupy import Component, Fragment, View, elements
from markupy.exceptions import MarkupyError


class ComponentElement(Component):
    def __init__(self, id: str):
        self.id = id

    def render(self) -> View:
        return elements.Div(id=self.id)


def test_component_element() -> None:
    assert ComponentElement("component") == """<div id="component"></div>"""


class ComponentFragment(Component):
    def render(self) -> View:
        return Fragment[elements.Div, elements.Img]


def test_uninitialized_component() -> None:
    with pytest.raises(MarkupyError):
        elements.P[ComponentFragment]


def test_component_fragment() -> None:
    assert ComponentFragment() == """<div></div><img>"""


class ComponentInComponent(Component):
    def render(self) -> View:
        return Fragment[elements.Input, ComponentElement("inside")]


def test_component_in_component() -> None:
    assert ComponentInComponent() == """<input><div id="inside"></div>"""


class ComponentAsComponent(Component):
    def render(self) -> View:
        return ComponentElement("other")


def test_component_as_component() -> None:
    assert ComponentAsComponent() == """<div id="other"></div>"""


class ContentComponent(Component):
    def __init__(self, id: str) -> None:
        super().__init__()
        self.id = id

    def render(self) -> View:
        return elements.H1(".title.header", id=self.id)[self.render_content()]


def test_component_content() -> None:
    assert (
        ContentComponent(id="test")["Hello", elements.Div[elements.Input]]
        == """<h1 class="title header" id="test">Hello<div><input></div></h1>"""
    )


def test_component_content_escape() -> None:
    # Make sure component contents are not re-escaped when assigned to element children
    assert (
        ContentComponent(id="test")['He>"llo']
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
        return elements.H1(id=self.id)


def test_super_error_component() -> None:
    assert SuperErrorComponent(id="foo") == """<h1 id="foo"></h1>"""
    with pytest.raises(MarkupyError):
        SuperErrorComponent(id="foo")["bar"]


@dataclass(eq=False)
class DataComponent(Component):
    href: str = field(default="https://google.com")

    def render(self) -> View:
        return elements.A(href=self.href)[self.render_content()]


def test_dataclass_component() -> None:
    result = """<a href="https://google.com">Google</a>"""
    assert DataComponent()["Google"] == result
