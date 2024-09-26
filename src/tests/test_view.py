from markupy import Node, View, tag


class ComponentElement(View):
    def render(self) -> Node:
        return tag.Div


class ComponentElementMultiple(View):
    def render(self) -> Node:
        return tag.Div, tag.Img


class ComponentInComponent(View):
    def render(self) -> Node:
        return tag.Input, ComponentElement()


def test_component_element() -> None:
    assert str(ComponentElement()) == """<div></div>"""


def test_component_element_multiple() -> None:
    assert str(ComponentElementMultiple()) == """<div></div><img>"""


def test_component_in_component() -> None:
    assert str(ComponentInComponent()) == """<input><div></div>"""
