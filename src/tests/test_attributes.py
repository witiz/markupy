import typing as t
from datetime import date

import pytest
from markupsafe import Markup

from markupy import attributes as attr
from markupy import elements as el
from markupy.exceptions import MarkupyError


def test_order() -> None:
    with pytest.raises(MarkupyError):
        el.Input({"foo": "bar"}, "selector")  # type: ignore
    with pytest.raises(MarkupyError):
        el.Input(attr.id("cool"), {"foo": "bar"})  # type: ignore
    with pytest.raises(MarkupyError):
        el.Input(attr.disabled(), "#foo.bar")  # type: ignore


def test_attribute_equivalence() -> None:
    obj = el.Input(attr.onclick("console.log('yo')"), attr.disabled())
    dct = el.Input({"onclick": "console.log('yo')", "disabled": True})
    kwd = el.Input(onclick="console.log('yo')", disabled=True)
    assert obj == dct == kwd


def test_comment_attributes() -> None:
    with pytest.raises(MarkupyError):
        el._(attr="foo")


def test_underscore_replacement() -> None:
    result = """<button hx-post="/foo" _="bar" whatever="ok">click me!</button>"""
    assert el.Button(hx_post="/foo", _="bar", whatever_="ok")["click me!"] == result


class Test_value_escape:
    pytestmark = pytest.mark.parametrize(
        "value",
        [
            '.<"foo',
            Markup('.<"foo'),
        ],
    )

    def test_selector(self, value: str) -> None:
        assert el.Div(value) == """<div class="&lt;&#34;foo"></div>"""

    def test_dict(self, value: str) -> None:
        assert el.Div({"bar": value}) == """<div bar=".&lt;&#34;foo"></div>"""

    def test_kwarg(self, value: str) -> None:
        assert el.Div(**{"bar": value}) == """<div bar=".&lt;&#34;foo"></div>"""


def test_boolean_attribute() -> None:
    assert el.Input(disabled="whatever") == """<input disabled="whatever">"""
    assert el.Input(disabled=0) == """<input disabled="0">"""


def test_boolean_attribute_true() -> None:
    assert el.Button(disabled=True) == "<button disabled></button>"


def test_boolean_attribute_false() -> None:
    assert el.Button(disabled=False) == "<button></button>"


def test_selector_and_kwargs() -> None:
    result = """<div id="theid" for="hello" data-foo="&lt;bar"></div>"""
    assert el.Div("#theid", for_="hello", data_foo="<bar") == result


def test_class_priority() -> None:
    result = """<div class="selector dict obj kwarg"></div>"""
    assert (
        el.Div(".selector", {"class": "dict"}, attr.class_("obj"), class_="kwarg")
        == result
    )


@pytest.mark.parametrize("not_an_attr", [1234, b"foo", object(), object, 1, 0, None])
def test_invalid_attribute_key(not_an_attr: t.Any) -> None:
    with pytest.raises(MarkupyError):
        el.Div({not_an_attr: "foo"})
    with pytest.raises(MarkupyError):
        el.Div(attr._(not_an_attr, "foo"))


@pytest.mark.parametrize(
    "not_an_attr",
    [b"foo", object(), object],
)
def test_invalid_attribute_value(not_an_attr: t.Any) -> None:
    with pytest.raises(MarkupyError):
        el.Div(foo=not_an_attr)
    with pytest.raises(MarkupyError):
        el.Div(attr.foo(not_an_attr))
    with pytest.raises(MarkupyError):
        el.Div({"foo": not_an_attr})


def test_attribute_redefinition() -> None:
    with pytest.raises(MarkupyError):
        el.Div(id="hello")(class_="world")


@pytest.mark.parametrize(
    "key",
    ["", " ", "  foo  ", "bAr", "foo bar", '<"foo', Markup('<"foo'), date.today()],
)
def test_invalid_key(key: str) -> None:
    with pytest.raises(MarkupyError):
        el.Div(attr._(key, "bar"))
    with pytest.raises(MarkupyError):
        el.Div({key: "bar"})
    with pytest.raises((MarkupyError, TypeError)):
        el.Div(**{key: "bar"})


def test_duplicate() -> None:
    with pytest.raises(MarkupyError):
        el.Div("#foo", {"id": "bar"})
    with pytest.raises(MarkupyError):
        el.Div("#foo", attr.id("bar"))
    with pytest.raises(MarkupyError):
        el.Div("#foo", id="bar")
    with pytest.raises(MarkupyError):
        el.Div({"disabled": False}, attr.disabled(True))
    with pytest.raises(MarkupyError):
        el.Div({"disabled": False}, disabled=True)
    with pytest.raises(MarkupyError):
        el.Div(attr.disabled(False), disabled=True)
    with pytest.raises(MarkupyError):
        el.A(attr.href(""), href="")


def test_none_override() -> None:
    assert (
        el.Input({"class": None}, foo="bar", class_="baz")
        == """<input class="baz" foo="bar">"""
    )
