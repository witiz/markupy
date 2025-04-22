import pytest
from markupsafe import Markup

from markupy._private.element import (
    CommentElement,
    Element,
    HtmlElement,
    VoidElement,
)
from markupy.elements import Div, Hr, Html, Input, MyElement, Unknown, _
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


def test_element_repr() -> None:
    assert repr(Div("#a")) == """<markupy.Element.div>"""


def test_void_element_repr() -> None:
    assert repr(Hr("#a")) == """<markupy.VoidElement.hr>"""


def test_markup_str() -> None:
    result = str(Div(id="a"))
    assert isinstance(result, str)
    assert isinstance(result, Markup)
    assert result == '<div id="a"></div>'


def test_element_type() -> None:
    assert type(Unknown) is Element
    assert type(MyElement) is Element
    assert type(Div) is Element
    assert type(Input) is VoidElement
    assert type(Html) is HtmlElement
    assert type(_) is CommentElement


def test_comment() -> None:
    assert _["Hello"] == "<!--Hello-->"
    assert _[Div["Hello"]] == "<!--<div>Hello</div>-->"


def test_attributes_after_children() -> None:
    with pytest.raises(MarkupyError):
        Div["hello"](id="world")
