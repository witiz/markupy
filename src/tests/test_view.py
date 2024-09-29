from markupy import Component, Node, tag


class ComponentElement(Component):
    def render(self) -> Node:
        return tag.Div


class ComponentElementMultiple(Component):
    def render(self) -> Node:
        return tag.Div, tag.Img


class ComponentInComponent(Component):
    def render(self) -> Node:
        return tag.Input, tag.Div("#parent")[ComponentElement()]


def test_component_element() -> None:
    assert str(ComponentElement()) == """<div></div>"""


def test_component_element_multiple() -> None:
    assert str(ComponentElementMultiple()) == """<div></div><img>"""


def test_component_in_component() -> None:
    assert (
        str(ComponentInComponent()) == """<input><div id="parent"><div></div></div>"""
    )
