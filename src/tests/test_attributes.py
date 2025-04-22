import typing as t
from datetime import date

import pytest
from markupsafe import Markup

from markupy import attributes as attr
from markupy.elements import Button, Div, Input, _
from markupy.exceptions import MarkupyError


def test_order() -> None:
    with pytest.raises(MarkupyError):
        Input({"foo": "bar"}, "selector")  # type: ignore
    with pytest.raises(MarkupyError):
        Input(attr.id("cool"), {"foo": "bar"})  # type: ignore
    with pytest.raises(MarkupyError):
        Input(attr.disabled(), "#foo.bar")  # type: ignore


def test_comment() -> None:
    with pytest.raises(MarkupyError):
        _(attr="foo")


def test_underscore_replacement() -> None:
    result = Button(hx_post="/foo", _="bar", whatever_="ok")["click me!"]
    assert (
        result == """<button hx-post="/foo" _="bar" whatever="ok">click me!</button>"""
    )


class Test_value_escape:
    pytestmark = pytest.mark.parametrize(
        "value",
        [
            '.<"foo',
            Markup('.<"foo'),
        ],
    )

    def test_selector(self, value: str) -> None:
        result = Div(value)
        assert result == """<div class="&lt;&#34;foo"></div>"""

    def test_dict(self, value: str) -> None:
        result = Div({"bar": value})
        assert result == """<div bar=".&lt;&#34;foo"></div>"""

    def test_kwarg(self, value: str) -> None:
        result = Div(**{"bar": value})
        assert result == """<div bar=".&lt;&#34;foo"></div>"""


def test_boolean_attribute() -> None:
    assert Input(disabled="whatever") == """<input disabled="whatever">"""
    assert Input(disabled=0) == """<input disabled="0">"""


def test_boolean_attribute_true() -> None:
    result = Button(disabled=True)
    assert result == "<button disabled></button>"


def test_boolean_attribute_false() -> None:
    result = Button(disabled=False)
    assert result == "<button></button>"


def test_selector_and_kwargs() -> None:
    result = Div("#theid", for_="hello", data_foo="<bar")
    assert result == """<div id="theid" for="hello" data-foo="&lt;bar"></div>"""


def test_attrs_and_kwargs() -> None:
    result = Div({"a": "1", "for": "a"}, for_="b", b="2")
    assert result == """<div a="1" for="b" b="2"></div>"""


def test_class_priority() -> None:
    result = Div(".selector", {"class": "dict"}, attr.class_("obj"), class_="kwarg")
    assert result == """<div class="selector dict obj kwarg"></div>"""


def test_id_priority() -> None:
    result = Div("#selector", {"id": "dict"}, attr.id("obj"), id="kwarg")
    assert result == """<div id="kwarg"></div>"""
    result = Div("#selector", {"id": "dict"}, attr.id("obj"))
    assert result == """<div id="obj"></div>"""
    result = Div("#selector", {"id": "dict"})
    assert result == """<div id="dict"></div>"""


@pytest.mark.parametrize("not_an_attr", [1234, b"foo", object(), object, 1, 0, None])
def test_invalid_attribute_key(not_an_attr: t.Any) -> None:
    with pytest.raises(MarkupyError):
        Div({not_an_attr: "foo"})


@pytest.mark.parametrize(
    "not_an_attr",
    [b"foo", object(), object],
)
def test_invalid_attribute_value(not_an_attr: t.Any) -> None:
    with pytest.raises(MarkupyError):
        Div(foo=not_an_attr)


def test_attribute_redefinition() -> None:
    with pytest.raises(MarkupyError):
        Div(id="hello")(class_="world")


@pytest.mark.parametrize(
    "key",
    ["", "  foo  ", "foo bar", '<"foo', Markup('<"foo'), date.today()],
)
def test_invalid_key(key: str) -> None:
    with pytest.raises(MarkupyError):
        Div({key: "bar"})
    with pytest.raises((MarkupyError, TypeError)):
        Div(**{key: "bar"})


def test_attribute_case() -> None:
    result = Div({"BAR": "foo", "bAr": "hello"}, bar="baz")
    # If not properly managed, could become <div BAR="foo" bar="baz"></div>
    assert result == """<div bar="baz"></div>"""
