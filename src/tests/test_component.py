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


def test_component_element() -> None:
    assert str(ComponentElement("component")) == """<div id="component"></div>"""


def test_component_fragment() -> None:
    assert str(ComponentFragment()) == """<div></div><img>"""


def test_component_in_component() -> None:
    assert str(ComponentInComponent()) == """<input><div id="inside"></div>"""


def test_component_as_component() -> None:
    assert str(ComponentAsComponent()) == """<div id="other"></div>"""


def test_uninitialized_component() -> None:
    with pytest.raises(MarkupyError):
        tag.P[ComponentFragment]
