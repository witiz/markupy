import typing as t
from datetime import date

import pytest
from markupsafe import Markup

from markupy.exception import MarkupyError
from markupy.tag import Button, Div, Input, Th, _


def test_attribute() -> None:
    assert str(Input(attr="disabled")) == '<input attr="disabled">'
    assert str(Input(disabled="disabled")) == "<input disabled>"


def test_true_value() -> None:
    assert str(Input(disabled=True)) == "<input disabled>"
    assert str(Input(disabled=1)) == "<input disabled>"
    assert str(Input(attr=True)) == "<input attr>"
    assert str(Input(attr=1)) == '<input attr="1">'


def test_false_value() -> None:
    assert str(Input(disabled=False)) == "<input>"
    assert str(Input(disabled=0)) == "<input>"
    assert str(Input(attr=False)) == "<input>"
    assert str(Input(attr=0)) == '<input attr="0">'


def test_none_value() -> None:
    assert str(Input(disabled=None)) == "<input>"
    assert str(Input(attr=None)) == "<input>"


def test_empty_value() -> None:
    # Different behaviour for boolean attributes vs regular
    assert str(Input(disabled="")) == """<input disabled>"""
    assert str(Input(attr="")) == """<input attr="">"""
    assert str(Input(id="", class_="")) == """<input>"""


def test_comment() -> None:
    with pytest.raises(MarkupyError):
        _(attr="foo")


class Test_class_names:
    def test_str(self) -> None:
        result = Div(class_='">foo bar')
        assert str(result) == '<div class="&#34;&gt;foo bar"></div>'

    def test_safestring(self) -> None:
        result = Div(class_=Markup('">foo bar'))
        assert str(result) == '<div class="&#34;&gt;foo bar"></div>'

    def test_list(self) -> None:
        result = Div(class_=['">foo', Markup('">bar'), None, "", "baz"])
        assert str(result) == '<div class="&#34;&gt;foo &#34;&gt;bar baz"></div>'

    def test_tuple(self) -> None:
        result = Div(class_=('">foo', Markup('">bar'), None, "", "baz"))
        assert str(result) == '<div class="&#34;&gt;foo &#34;&gt;bar baz"></div>'

    def test_dict(self) -> None:
        result = Div(
            class_={'">foo': True, Markup('">bar'): True, "x": False, "baz": True}
        )
        assert str(result) == '<div class="&#34;&gt;foo &#34;&gt;bar baz"></div>'

    def test_nested_dict(self) -> None:
        result = Div(
            class_=[
                '">list-foo',
                Markup('">list-bar'),
                {'">dict-foo': True, Markup('">list-bar'): True, "x": False},
            ]
        )
        assert (
            str(result)
            == """<div class="&#34;&gt;list-foo &#34;&gt;list-bar &#34;&gt;dict-foo &#34;&gt;list-bar"></div>"""
        )

    def test_false(self) -> None:
        result = str(Div(class_=False))
        assert result == "<div></div>"

    def test_none(self) -> None:
        result = str(Div(class_=None))
        assert result == "<div></div>"

    def test_no_classes(self) -> None:
        result = str(Div(class_={"foo": False}))
        assert result == "<div></div>"

    def test_selector_attr_mixed(self) -> None:
        result = str(Div(".foo", class_={"bar": True, "baz": False}))
        assert result == """<div class="foo bar"></div>"""


def test_dict_attributes() -> None:
    result = Div({"@click": 'hi = "hello"'})

    assert str(result) == """<div @click="hi = &#34;hello&#34;"></div>"""


def test_underscore() -> None:
    # Hyperscript (https://hyperscript.org/) uses _, make sure it works good.
    result = Div(_="foo")
    assert str(result) == """<div _="foo"></div>"""


def test_dict_attributes_avoid_replace() -> None:
    result = Div({"class_": "foo", "hello_hi": "abc"})
    assert str(result) == """<div class_="foo" hello_hi="abc"></div>"""


def test_dict_attribute_false() -> None:
    result = Div({"bool-false": False})
    assert str(result) == "<div></div>"


def test_dict_attribute_true() -> None:
    result = Div({"bool-true": True})
    assert str(result) == "<div bool-true></div>"


def test_uppercase_replacement() -> None:
    result = Button(hxPost="/foo")["click me!"]
    assert str(result) == """<button hx-post="/foo">click me!</button>"""


def test_at_replacement() -> None:
    result = Input(_input_debounce_500ms="fetchResults")
    assert str(result) == """<input @input.debounce.500ms="fetchResults">"""


def test_colon_replacement() -> None:
    result = Button(
        hxOn__htmx__configRequest="event.detail.parameters.example = 'Hello Scripting!'"
    )["Post Me!"]
    assert (
        str(result)
        == """<button hx-on:htmx:config-request="event.detail.parameters.example = &#39;Hello Scripting!&#39;">Post Me!</button>"""
    )


class Test_value_escape:
    pytestmark = pytest.mark.parametrize(
        "value",
        [
            '<"foo',
            Markup('<"foo'),
        ],
    )

    def test_dict(self, value: str) -> None:
        result = Div({"bar": value})
        assert str(result) == """<div bar="&lt;&#34;foo"></div>"""

    def test_kwarg(self, value: str) -> None:
        result = Div(**{"bar": value})
        assert str(result) == """<div bar="&lt;&#34;foo"></div>"""


def test_boolean_attribute_true() -> None:
    result = Button(disabled=True)
    assert str(result) == "<button disabled></button>"


def test_kwarg_attribute_none() -> None:
    result = Div(foo=None)
    assert str(result) == "<div></div>"


def test_dict_attribute_none() -> None:
    result = Div({"foo": None})
    assert str(result) == "<div></div>"


def test_boolean_attribute_false() -> None:
    result = Button(disabled=False)
    assert str(result) == "<button></button>"


def test_integer_attribute() -> None:
    result = Th(colspan=123, tabindex=0)
    assert str(result) == '<th colspan="123" tabindex="0"></th>'


def test_selector() -> None:
    result = Div("#myid.cls1.cls2")

    assert str(result) == """<div id="myid" class="cls1 cls2"></div>"""


def test_selector_only_id() -> None:
    result = Div("#myid")
    assert str(result) == """<div id="myid"></div>"""


def test_selector_only_classes() -> None:
    result = Div(".foo.bar")
    assert str(result) == """<div class="foo bar"></div>"""


def test_selector_empty_classes() -> None:
    result = Div(".foo..bar.")
    assert str(result) == """<div class="foo bar"></div>"""


def test_selector_classes_space_separator() -> None:
    result = Div("foo bar")
    assert str(result) == """<div class="foo bar"></div>"""


def test_selector_bad_type() -> None:
    with pytest.raises(MarkupyError):
        Div({"oops": "yes"}, {})  # type: ignore


def test_invalid_number_of_attributes() -> None:
    with pytest.raises(MarkupyError):
        Div("#id.cls", {"attr": "val"}, "other")  # type: ignore


def test_id_class_and_kwargs() -> None:
    result = Div("#theid", for_="hello", dataFoo="<bar")
    assert str(result) == """<div id="theid" for="hello" data-foo="&lt;bar"></div>"""


def test_attrs_and_kwargs() -> None:
    result = Div({"a": "1", "for": "a"}, for_="b", b="2")
    assert str(result) == """<div a="1" for="b" b="2"></div>"""


def test_class_priority() -> None:
    result = Div(".a", {"class": "b"}, class_="c")
    assert str(result) == """<div class="a b c"></div>"""

    result = Div(".a", {"class": "b"})
    assert str(result) == """<div class="a b"></div>"""


def test_attribute_priority() -> None:
    result = Div({"foo": "a"}, foo="b")
    assert str(result) == """<div foo="b"></div>"""


@pytest.mark.parametrize("not_an_attr", [1234, b"foo", object(), object, 1, 0, None])
def test_invalid_attribute_key(not_an_attr: t.Any) -> None:
    with pytest.raises(MarkupyError):
        str(Div({not_an_attr: "foo"}))


@pytest.mark.parametrize(
    "not_an_attr",
    [12.34, b"foo", object(), object],
)
def test_invalid_attribute_value(not_an_attr: t.Any) -> None:
    with pytest.raises(MarkupyError):
        Div(foo=not_an_attr)


def test_attribute_redefinition() -> None:
    with pytest.raises(MarkupyError):
        Div(id="hello")(class_="world")


@pytest.mark.parametrize("selector", ["", "   ", "  #  ", "  .  "])
def test_empty_selector(selector: str) -> None:
    result = Div(selector)
    assert str(result) == """<div></div>"""


def test_selector_strip() -> None:
    result = Div(" #myid .myclass .other ")
    assert str(result) == """<div id="myid" class="myclass other"></div>"""


@pytest.mark.parametrize(
    "key",
    ["", "  foo  ", "foo bar", '<"foo', Markup('<"foo'), date.today()],
)
def test_invalid_key(key: str) -> None:
    with pytest.raises(MarkupyError):
        Div({key: "bar"})
    with pytest.raises((MarkupyError, TypeError)):
        Div(**{key: "bar"})


def test_attribute_case() -> None:
    result = Div({"BAR": "foo", "bAr": "hello"}, bar="baz")
    # If not properly managed, could become <div BAR="foo" bar="baz"></div>
    assert str(result) == """<div bar="baz"></div>"""


def test_selector_invalid_id_position() -> None:
    with pytest.raises(MarkupyError):
        Div(".bar#foo")


def test_selector_multiple_id() -> None:
    with pytest.raises(MarkupyError):
        Div("#foo#bar")


def test_selector_empty_id() -> None:
    assert str(Div("# foo bar")) == """<div class="foo bar"></div>"""
    assert str(Div("#.foo.bar")) == """<div class="foo bar"></div>"""
