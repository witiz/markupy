from markupy import Fragment, View
from markupy import elements as el


def test_empty_view() -> None:
    assert View() == ""


def test_equalty() -> None:
    assert View() == View()
    assert View() == ""
    assert View() == Fragment[""]
    assert View() != el.Input
    assert el.P("#foo.bar", hello="world") == el.P("#foo.bar", hello="world")
