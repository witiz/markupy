from markupy._private.node import iter_node
from markupy.tag import Div, Tr


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
