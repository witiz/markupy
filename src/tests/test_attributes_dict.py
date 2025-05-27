from markupy.elements import Div


def test_redefinition() -> None:
    result = """<div attr="val" attr2="val2"></div>"""
    assert result == Div({"attr": "val"}, {"attr2": "val2"})


def test_dict_attributes_escape() -> None:
    result = Div({"@click": 'hi = "hello"'})
    assert result == """<div @click="hi = &#34;hello&#34;"></div>"""


def test_dict_attributes_avoid_replace() -> None:
    result = Div({"class_": "foo", "hello_hi": "abc"})
    assert result == """<div class_="foo" hello_hi="abc"></div>"""


def test_dict_attribute_false() -> None:
    result = Div({"bool-false": False})
    assert result == "<div></div>"


def test_dict_attribute_true() -> None:
    result = Div({"bool-true": True})
    assert result == "<div bool-true></div>"


def test_dict_attribute_none() -> None:
    result = Div({"foo": None})
    assert result == "<div></div>"
