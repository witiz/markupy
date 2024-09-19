from markupsafe import Markup

from markupy.element import (
    CommentElement,
    Element,
    HtmlElement,
    VoidElement,
)
from markupy.tag import Div, Hr, Html, Input, _, __


def test_instance_cache() -> None:
    """
    markupy creates element object dynamically. make sure they are reused.
    """
    from markupy import tag

    assert tag.div is tag.div
    assert tag.Div is tag.Div
    assert tag.div is tag.div()
    assert tag.div is tag.div(attr=False)
    assert tag.div is not tag.div[None]


def test_element_repr() -> None:
    assert repr(Div("#a")) == """<Element '<div id="a">'>"""


def test_void_element_repr() -> None:
    assert repr(Hr("#a")) == """<VoidElement '<hr id="a">'>"""


def test_markup_str() -> None:
    result = str(Div(id="a"))
    assert isinstance(result, str)
    assert isinstance(result, Markup)
    assert result == '<div id="a"></div>'


def test_element_type() -> None:
    assert type(Div) is Element
    assert type(Input) is VoidElement
    assert type(Html) is HtmlElement
    assert type(_) is CommentElement
    assert type(__) is CommentElement


def test_comment() -> None:
    assert str(_["Hello"]) == "<!--Hello-->"
    assert str(_[Div["Hello"]]) == "<!--<div>Hello</div>-->"
