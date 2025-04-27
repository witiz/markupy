from __future__ import annotations

import typing as t

import pytest
from markupsafe import Markup

from markupy._private.views.element import Element, VoidElement
from markupy.elements import (
    Dd,
    Div,
    Dl,
    Dt,
    Html,
    Img,
    Input,
    Li,
    MyCustomElement,
    Script,
    Style,
    Ul,
)
from markupy.exceptions import MarkupyError

if t.TYPE_CHECKING:
    from collections.abc import Generator


def test_void_element() -> None:
    element = Input(name="foo")
    assert isinstance(element, VoidElement)

    result = element
    assert result == '<input name="foo">'

    with pytest.raises(MarkupyError):
        element["child"]


def test_safe_script_element() -> None:
    # The ' quotes don't get escaped
    result = """<script type="text/javascript">alert('test');</script>"""
    assert Script(type="text/javascript")["alert('test');"] == result


def test_safe_style_element() -> None:
    # The > symbol doesn't get escaped
    result = """<style type="text/css">body>.test {color:red}</style>"""
    assert Style(type="text/css")["body>.test {color:red}"] == result


def test_children() -> None:
    assert Div[Img] == "<div><img></div>"


def test_integer_child() -> None:
    assert Div[123] == "<div>123</div>"


def test_multiple_children() -> None:
    result = Ul[Li, Li]

    assert result == "<ul><li></li><li></li></ul>"


def test_list_children() -> None:
    children: list[Element] = [Li["a"], Li["b"]]
    result = Ul[children]
    assert result == "<ul><li>a</li><li>b</li></ul>"


def test_list_children_with_element_and_none() -> None:
    children: list[t.Any] = [None, Li["b"]]
    result = Ul[children]
    assert result == "<ul><li>b</li></ul>"


def test_list_children_with_none() -> None:
    children: list[t.Any] = [None]
    result = Ul[children]
    assert result == "<ul></ul>"


def test_tuple_children() -> None:
    result = Ul[(Li["a"], Li["b"])]
    assert result == "<ul><li>a</li><li>b</li></ul>"


def test_flatten_nested_children() -> None:
    result = Dl[
        [
            (Dt["a"], Dd["b"]),
            (Dt["c"], Dd["d"]),
        ]
    ]
    assert result == """<dl><dt>a</dt><dd>b</dd><dt>c</dt><dd>d</dd></dl>"""


def test_flatten_very_nested_children() -> None:
    # maybe not super useful but the nesting may be arbitrarily deep
    result = Div[[([["a"]],)], [([["b"]],)]]
    assert result == """<div>ab</div>"""


def test_flatten_nested_generators() -> None:
    def cols() -> Generator[str, None, None]:
        yield "a"
        yield "b"
        yield "c"

    def rows() -> Generator[Generator[str, None, None], None, None]:
        yield cols()
        yield cols()
        yield cols()

    result = Div[rows()]

    assert result == """<div>abcabcabc</div>"""


def test_generator_children() -> None:
    gen: Generator[Element, None, None] = (Li[x] for x in ["a", "b"])
    result = Ul[gen]
    assert result == "<ul><li>a</li><li>b</li></ul>"


def test_generator_exhaustion() -> None:
    top_three = Ul[(Li[i] for i in range(1, 4))]
    result = "<ul><li>1</li><li>2</li><li>3</li></ul>"
    assert top_three == result
    # we make sure rendering is not impacted by generator exhaustion after initial run
    assert top_three == result


def test_html_tag_with_doctype() -> None:
    result = Html(foo="bar")["hello"]
    assert result == '<!doctype html><html foo="bar">hello</html>'


def test_void_element_children() -> None:
    with pytest.raises(MarkupyError):
        Img["hey"]


def test_call_without_args() -> None:
    result = Img()
    assert result == "<img>"


def test_custom_element() -> None:
    el = MyCustomElement()
    assert isinstance(el, Element)
    assert el == "<my-custom-element></my-custom-element>"


@pytest.mark.parametrize("ignored_value", [None, True, False])
def test_ignored(ignored_value: t.Any) -> None:
    assert Div[ignored_value] == "<div></div>"


def test_iter_str() -> None:
    _, child, _ = Div["a"]

    assert child == "a"
    # Make sure we dont get Markup (subclass of str)
    assert type(child) is str


def test_iter_markup() -> None:
    _, child, _ = Div["a"]

    assert child == "a"
    # Make sure we dont get Markup (subclass of str)
    assert type(child) is str


def test_escape_children() -> None:
    result = Div['>"']
    assert result == "<div>&gt;&#34;</div>"


def test_safe_children() -> None:
    result = Div[Markup("<hello></hello>")]
    assert result == "<div><hello></hello></div>"


def test_children_redefinition() -> None:
    with pytest.raises(MarkupyError):
        Div["Hello"]["World"]


def test_callable() -> None:
    def hello() -> str:
        return "world"

    with pytest.raises(MarkupyError):
        Div[hello]
