import pytest

from markupy import Component, Fragment, View, tag
from markupy.exception import MarkupyError


class ComponentElement(Component):
    def __init__(self, id: str):
        self.id = id

    def render(self) -> View:
        return tag.Div(id=self.id)


class ComponentFragment(Component):
    def render(self) -> View:
        return Fragment[tag.Div, tag.Img]


class ComponentInComponent(Component):
    def render(self) -> View:
        return Fragment[tag.Input, ComponentElement("inside")]


class ComponentAsComponent(Component):
    def render(self) -> View:
        return ComponentElement("other")


class ContentComponent(Component):
    def __init__(self, id: str) -> None:
        super().__init__()
        self.id = id

    def render(self) -> View:
        return tag.H1(".title.header", id=self.id)[self.render_content()]


def test_component_element() -> None:
    assert str(ComponentElement("component")) == """<div id="component"></div>"""


def test_component_fragment() -> None:
    assert str(ComponentFragment()) == """<div></div><img>"""


def test_component_in_component() -> None:
    assert str(ComponentInComponent()) == """<input><div id="inside"></div>"""


def test_component_as_component() -> None:
    assert str(ComponentAsComponent()) == """<div id="other"></div>"""


def test_component_content() -> None:
    assert (
        str(ContentComponent(id="test")["Hello", tag.Div[tag.Input]])
        == """<h1 class="title header" id="test">Hello<div><input></div></h1>"""
    )


def test_uninitialized_component() -> None:
    with pytest.raises(MarkupyError):
        tag.P[ComponentFragment]
