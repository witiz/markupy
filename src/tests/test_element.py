import pytest
from markupsafe import Markup

from markupy import elements as el
from markupy._private.views.element import (
    CommentElement,
    Element,
    HtmlElement,
    VoidElement,
)
from markupy.exceptions import MarkupyError


def test_instance_cache() -> None:
    """
    markupy creates element object dynamically. make sure they are reused.
    """
    assert el.Div is el.Div
    assert el.Div is el.Div()
    assert el.Div is el.Div("", {}, None, attr1=None, attr2=False)
    assert el.Div is el.Div[None]
    assert el.Div is el.Div[True]
    assert el.Div is el.Div[False]
    assert el.Div is el.Div[[]]
    assert el.Div is el.Div[[None]]
    assert el.Div is el.Div[""]
    assert el.Div is not el.Div[0]


def test_invalid_case() -> None:
    with pytest.raises(MarkupyError):
        el.div
    with pytest.raises(MarkupyError):
        el.My_Div


def test_name() -> None:
    assert el.SlInput == "<sl-input></sl-input>"
    assert el.XInput == "<x-input></x-input>"
    assert el.X1Input == "<x1-input></x1-input>"


def test_element_repr() -> None:
    assert repr(el.Div("#a")) == """<markupy.Element.div>"""


def test_void_element_repr() -> None:
    assert repr(el.Hr("#a")) == """<markupy.VoidElement.hr>"""


def test_markup_str() -> None:
    result = str(el.Div(id="a"))
    assert isinstance(result, str)
    assert isinstance(result, Markup)
    assert result == '<div id="a"></div>'


def test_element_type() -> None:
    assert type(el.Unknown) is Element
    assert type(el.MyElement) is Element
    assert type(el.Div) is Element
    assert type(el.Input) is VoidElement
    assert type(el.Html) is HtmlElement
    assert type(el._) is CommentElement


def test_comment() -> None:
    assert el._["Hello"] == "<!--Hello-->"
    assert el._[el.Div["Hello"]] == "<!--<div>Hello</div>-->"


def test_attributes_after_children() -> None:
    with pytest.raises(MarkupyError):
        el.Div["hello"](id="world")
