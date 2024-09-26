from typing import Any

from markupsafe import Markup

from markupy import View
from markupy.tag import Div, Tr


def assert_markup(result: Any, expected: str) -> None:
    assert isinstance(result, Markup)
    assert result == expected


class Test_render_node:
    def test_render(self) -> None:
        view = View(Div["a"])
        assert str(view) == view.render()

    def test_element(self) -> None:
        result = View(Div["a"]).render()
        assert_markup(result, "<div>a</div>")

    def test_list(self) -> None:
        result = View([Tr["a"], Tr["b"]]).render()

        assert_markup(result, "<tr>a</tr><tr>b</tr>")

    def test_none(self) -> None:
        result = View(None).render()
        assert_markup(result, "")

    def test_string(self) -> None:
        result = View("hello!").render()
        assert_markup(result, "hello!")


class Test_iter_node:
    def test_element(self) -> None:
        result = list(View(Div["a"]))

        # Ensure we get str back, not markup.
        assert type(result[0]) is str
        assert result == ["<div>", "a", "</div>"]

    def test_multiple_elements(self) -> None:
        result = list(View(Tr["a"], Tr["b"]))
        assert result == ["<tr>", "a", "</tr>", "<tr>", "b", "</tr>"]

    def test_list(self) -> None:
        result = list(View([Tr["a"], Tr["b"]]))
        assert result == ["<tr>", "a", "</tr>", "<tr>", "b", "</tr>"]

    def test_none(self) -> None:
        result = list(View(None))
        assert result == []

    def test_string(self) -> None:
        result = list(View("yo!"))
        assert result == ["yo!"]
