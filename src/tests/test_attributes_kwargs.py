from markupsafe import Markup

from markupy.elements import Div, Input, Th

# from markupy.exceptions import MarkupyError


def test_kwarg_attribute_none() -> None:
    result = Div(foo=None)
    assert str(result) == "<div></div>"


def test_underscore() -> None:
    # Hyperscript (https://hyperscript.org/) uses _, make sure it works good.
    result = Div(_="foo")
    assert str(result) == """<div _="foo"></div>"""


def test_true_value() -> None:
    assert str(Input(disabled=True)) == "<input disabled>"
    assert str(Input(attr=True)) == "<input attr>"


def test_false_value() -> None:
    assert str(Input(disabled=False)) == "<input>"
    assert str(Input(attr=False)) == "<input>"


def test_none_value() -> None:
    assert str(Input(disabled=None)) == "<input>"
    assert str(Input(attr=None)) == "<input>"


def test_empty_value() -> None:
    # Different behaviour for boolean attributes vs regular
    assert str(Input(disabled="")) == """<input disabled="">"""
    assert str(Input(attr="")) == """<input attr="">"""
    assert str(Input(id="", class_="", name="")) == """<input id="" class="" name="">"""


def test_integer_attribute() -> None:
    result = Th(colspan=123, tabindex=0)
    assert str(result) == '<th colspan="123" tabindex="0"></th>'


def test_float_attribute() -> None:
    result = Input(value=37.2)
    assert str(result) == '<input value="37.2">'


class Test_class_names:
    def test_str(self) -> None:
        result = Div(class_='">foo bar')
        assert str(result) == '<div class="&#34;&gt;foo bar"></div>'

    def test_safestring(self) -> None:
        result = Div(class_=Markup('">foo bar'))
        assert str(result) == '<div class="&#34;&gt;foo bar"></div>'

    def test_false(self) -> None:
        result = str(Div(class_=False))
        assert result == "<div></div>"

    def test_none(self) -> None:
        result = str(Div(class_=None))
        assert result == "<div></div>"
