from typing import Any

from markupsafe import Markup

from markupy._private.node import iter_node, render_node
from markupy.tag import Div, Tr


def assert_markup(result: Any, expected: str) -> None:
    assert isinstance(result, Markup)
    assert result == expected


class Test_render_node:
    def test_element(self) -> None:
        result = render_node(Div["a"])
        assert_markup(result, "<div>a</div>")

    def test_multiple_element(self) -> None:
        result = render_node(Tr["a"], Tr["b"])
        assert_markup(result, "<tr>a</tr><tr>b</tr>")

    def test_list(self) -> None:
        result = render_node([Tr["a"], Tr["b"]])
        assert_markup(result, "<tr>a</tr><tr>b</tr>")

    def test_none(self) -> None:
        result = render_node(None)
        assert_markup(result, "")

    def test_string(self) -> None:
        result = render_node("hello!")
        assert_markup(result, "hello!")


class Test_iter_node:
    def test_element(self) -> None:
        result = list(iter_node(Div["a"]))

        # Ensure we get str back, not markup.
        assert type(result[0]) is str
        assert result == ["<div>", "a", "</div>"]

    def test_list(self) -> None:
        result = list(iter_node([Tr["a"], Tr["b"]]))
        assert result == ["<tr>", "a", "</tr>", "<tr>", "b", "</tr>"]

    def test_none(self) -> None:
        result = list(iter_node(None))
        assert result == []

    def test_string(self) -> None:
        result = list(iter_node("yo!"))
        assert result == ["yo!"]
