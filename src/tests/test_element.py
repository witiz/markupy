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
    from markupy import elements

    assert elements.Div is elements.Div
    assert elements.Div is elements.Div()
    assert elements.Div is elements.Div(attr=False)
    assert elements.Div is elements.Div[None]
    assert elements.Div is elements.Div[True]
    assert elements.Div is elements.Div[False]
    assert elements.Div is elements.Div[[]]
    assert elements.Div is elements.Div[[None]]
    assert elements.Div is elements.Div[""]
    assert elements.Div is not elements.Div[0]


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
