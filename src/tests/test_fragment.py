from typing import Iterator

import pytest

from markupy import Fragment
from markupy.elements import Div, I, P, Tr
from markupy.exceptions import MarkupyError


def test_render_direct() -> None:
    assert Fragment["Hello ", None, I["World"]] == """Hello <i>World</i>"""


def test_render_as_child() -> None:
    assert (
        P["Say: ", Fragment["Hello ", None, I["World"]], "!"]
        == """<p>Say: Hello <i>World</i>!</p>"""
    )


def test_render_nested() -> None:
    assert Fragment[Fragment["Hel", "lo "], "World"] == """Hello World"""


def test_render_embedded() -> None:
    assert (
        P[Fragment["Good ", I["morning"]], " ", I["World"]]
        == """<p>Good <i>morning</i> <i>World</i></p>"""
    )


def test_safe() -> None:
    assert Fragment['>"'] == """&gt;&#34;"""


def test_iter() -> None:
    assert list(Fragment["Hello ", None, I["World"]]) == [
        "Hello ",
        "<i>",
        "World",
        "</i>",
    ]


def test_element() -> None:
    result = Fragment[Div["a"]]
    assert result == "<div>a</div>"


def test_multiple_element() -> None:
    result = Fragment[Tr["a"], Tr["b"]]
    assert result == "<tr>a</tr><tr>b</tr>"


def test_list() -> None:
    result = Fragment[[Tr["a"], Tr["b"]]]
    assert result == "<tr>a</tr><tr>b</tr>"


def test_none() -> None:
    result = Fragment[None]
    assert result == ""


def test_string() -> None:
    result = Fragment["hello!"]
    assert result == "hello!"


def test_class() -> None:
    class Test:
        def __call__(self) -> str:
            return self.message()

        def __str__(self) -> str:
            return self()

        def message(self) -> str:
            return "hello"

    assert Fragment[Test()] == "hello"
    assert Fragment[Test().message()] == "hello"
    with pytest.raises(MarkupyError):
        Fragment[Test]
    with pytest.raises(MarkupyError):
        Fragment[Test().message]


def test_lambda() -> None:
    with pytest.raises(MarkupyError):
        Fragment[lambda: "hello"]


def test_function() -> None:
    def test() -> str:
        return "hello"

    assert Fragment[test()] == "hello"
    with pytest.raises(MarkupyError):
        Fragment[test]


def test_generator() -> None:
    def generator() -> Iterator[str]:
        yield "hello"
        yield "world"

    assert Fragment[generator()] == "helloworld"
    with pytest.raises(MarkupyError):
        Fragment[generator]
