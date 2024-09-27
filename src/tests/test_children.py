from __future__ import annotations

import typing as t

import pytest
from markupsafe import Markup

from markupy._private.element import Element, VoidElement
from markupy.tag import (
    Dd,
    Div,
    Dl,
    Dt,
    Html,
    Img,
    Input,
    Li,
    MyCustomElement,
    Ul,
)

if t.TYPE_CHECKING:
    from collections.abc import Callable, Generator

    from markupy import Node


def test_void_element() -> None:
    element = Input(name="foo")
    assert isinstance(element, VoidElement)

    result = str(element)
    assert str(result) == '<input name="foo">'

    with pytest.raises(ValueError):
        element["child"]


def test_children() -> None:
    assert str(Div[Img]) == "<div><img></div>"


def test_integer_child() -> None:
    assert str(Div[123]) == "<div>123</div>"


def test_multiple_children() -> None:
    result = Ul[Li, Li]

    assert str(result) == "<ul><li></li><li></li></ul>"


def test_list_children() -> None:
    children: list[Element] = [Li["a"], Li["b"]]
    result = Ul[children]
    assert str(result) == "<ul><li>a</li><li>b</li></ul>"


def test_list_children_with_element_and_none() -> None:
    children: list[Node] = [None, Li["b"]]
    result = Ul[children]
    assert str(result) == "<ul><li>b</li></ul>"


def test_list_children_with_none() -> None:
    children: list[Node] = [None]
    result = Ul[children]
    assert str(result) == "<ul></ul>"


def test_tuple_children() -> None:
    result = Ul[(Li["a"], Li["b"])]
    assert str(result) == "<ul><li>a</li><li>b</li></ul>"


def test_flatten_nested_children() -> None:
    result = Dl[
        [
            (Dt["a"], Dd["b"]),
            (Dt["c"], Dd["d"]),
        ]
    ]
    assert str(result) == """<dl><dt>a</dt><dd>b</dd><dt>c</dt><dd>d</dd></dl>"""


def test_flatten_very_nested_children() -> None:
    # maybe not super useful but the nesting may be arbitrarily deep
    result = Div[[([["a"]],)], [([["b"]],)]]
    assert str(result) == """<div>ab</div>"""


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

    assert str(result) == """<div>abcabcabc</div>"""


def test_generator_children() -> None:
    gen: Generator[Element, None, None] = (Li[x] for x in ["a", "b"])
    result = Ul[gen]
    assert str(result) == "<ul><li>a</li><li>b</li></ul>"


def test_html_tag_with_doctype() -> None:
    result = Html(foo="bar")["hello"]
    assert str(result) == '<!doctype html><html foo="bar">hello</html>'


def test_void_element_children() -> None:
    with pytest.raises(ValueError):
        Img["hey"]


def test_call_without_args() -> None:
    result = Img()
    assert str(result) == "<img>"


def test_custom_element() -> None:
    el = MyCustomElement()
    assert isinstance(el, Element)
    assert str(el) == "<my-custom-element></my-custom-element>"


@pytest.mark.parametrize("ignored_value", [None, True, False])
def test_ignored(ignored_value: t.Any) -> None:
    assert str(Div[ignored_value]) == "<div></div>"


def test_iter() -> None:
    trace = "not started"

    def generate_list() -> Generator[Element, None, None]:
        nonlocal trace

        trace = "before yield"
        yield Li("#a")

        trace = "done"

    iterator = iter(Ul[generate_list()])

    assert next(iterator) == "<ul>"
    assert trace == "not started"

    assert next(iterator) == '<li id="a">'
    assert trace == "before yield"
    assert next(iterator) == "</li>"
    assert trace == "before yield"

    assert next(iterator) == "</ul>"
    assert trace == "done"


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


def test_callable() -> None:
    called = False

    def generate_img() -> Element:
        nonlocal called
        called = True
        return Img

    iterator = iter(Div[generate_img])

    assert next(iterator) == "<div>"
    assert called is False
    assert next(iterator) == "<img>"
    assert called is True
    assert next(iterator) == "</div>"


def test_escape_children() -> None:
    result = str(Div['>"'])
    assert result == "<div>&gt;&#34;</div>"


def test_safe_children() -> None:
    result = str(Div[Markup("<hello></hello>")])
    assert result == "<div><hello></hello></div>"


def test_nested_callable_generator() -> None:
    def func() -> Generator[str, None, None]:
        return (x for x in "abc")

    assert str(Div[func]) == "<div>abc</div>"


def test_nested_callables() -> None:
    def first() -> Callable[[], Node]:
        return second

    def second() -> Node:
        return "hi"

    assert str(Div[first]) == "<div>hi</div>"


def test_callable_in_generator() -> None:
    assert str(Div[((lambda: "hi") for _ in range(1))]) == "<div>hi</div>"


@pytest.mark.parametrize("not_a_child", [12.34, object(), object])
def test_invalid_child(not_a_child: t.Any) -> None:
    with pytest.raises(TypeError):
        str(Div[not_a_child])
