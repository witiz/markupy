import pytest

from markupy.elements import Div
from markupy.exceptions import MarkupyError


def test_redefinition() -> None:
    with pytest.raises(MarkupyError):
        Div("#id.cls", "#id2.cls2")  # type: ignore


def test_selector() -> None:
    result = Div("#myid.cls1.cls2")

    assert result == """<div id="myid" class="cls1 cls2"></div>"""


def test_selector_only_id() -> None:
    result = Div("#myid")
    assert result == """<div id="myid"></div>"""


def test_selector_only_classes() -> None:
    result = Div(".foo.bar")
    assert result == """<div class="foo bar"></div>"""


def test_selector_empty_classes() -> None:
    result = Div(".foo..bar.")
    assert result == """<div class="foo bar"></div>"""


def test_selector_classes_space_separator() -> None:
    result = Div("foo bar")
    assert result == """<div class="foo bar"></div>"""


def test_selector_bad_type() -> None:
    with pytest.raises(MarkupyError):
        Div({"oops": "yes"}, {})  # type: ignore


@pytest.mark.parametrize("selector", ["", "   ", "  #  ", "  .  ", "  #  .  "])
def test_empty_selector(selector: str) -> None:
    result = Div(selector)
    assert result == """<div></div>"""


def test_selector_strip() -> None:
    result = Div(" #myid .myclass .other ")
    assert result == """<div id="myid" class="myclass other"></div>"""


def test_selector_invalid_id_position() -> None:
    with pytest.raises(MarkupyError):
        Div(".bar#foo")


def test_selector_multiple_id() -> None:
    with pytest.raises(MarkupyError):
        Div("#foo#bar")


def test_selector_empty_id() -> None:
    assert Div("# foo bar") == """<div class="foo bar"></div>"""
    assert Div("#.foo.bar") == """<div class="foo bar"></div>"""
