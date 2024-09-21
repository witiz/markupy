import typing as t

import pytest
from markupsafe import Markup

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
    assert str(Input(disabled="")) == "<input disabled>"
    assert str(Input(attr="")) == "<input>"


def test_comment() -> None:
    with pytest.raises(ValueError):
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


class Test_attribute_escape:
    pytestmark = pytest.mark.parametrize(
        "x",
        [
            '<"foo',
            Markup('<"foo'),
        ],
    )

    def test_dict(self, x: str) -> None:
        result = Div({x: x})
        assert str(result) == """<div &lt;&#34;foo="&lt;&#34;foo"></div>"""

    def test_kwarg(self, x: str) -> None:
        result = Div(**{x: x})
        assert str(result) == """<div &lt;&#34;foo="&lt;&#34;foo"></div>"""


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


def test_id_class() -> None:
    result = Div("#myid.cls1.cls2")

    assert str(result) == """<div id="myid" class="cls1 cls2"></div>"""


def test_id_class_only_id() -> None:
    result = Div("#myid")
    assert str(result) == """<div id="myid"></div>"""


def test_id_class_only_classes() -> None:
    result = Div(".foo.bar")
    assert str(result) == """<div class="foo bar"></div>"""


def test_id_class_empty_classes() -> None:
    result = Div(".foo..bar.")
    assert str(result) == """<div class="foo bar"></div>"""


def test_id_class_bad_format() -> None:
    with pytest.raises(ValueError):
        Div("foo")


def test_id_class_bad_type() -> None:
    with pytest.raises(TypeError):
        Div({"oops": "yes"}, {})  # type: ignore


def test_invalid_number_of_attributes() -> None:
    with pytest.raises(ValueError):
        Div("#id.cls", {"attr": "val"}, "other")  # type: ignore


def test_id_class_and_kwargs() -> None:
    result = Div("#theid", for_="hello", dataFoo="<bar")
    assert str(result) == """<div id="theid" for="hello" data-foo="&lt;bar"></div>"""


def test_attrs_and_kwargs() -> None:
    result = Div({"a": "1", "for": "a"}, for_="b", b="2")
    assert str(result) == """<div a="1" for="b" b="2"></div>"""


def test_class_priority() -> None:
    result = Div(".a", {"class": "b"}, class_="c")
    assert str(result) == """<div class="c"></div>"""

    result = Div(".a", {"class": "b"})
    assert str(result) == """<div class="b"></div>"""


def test_attribute_priority() -> None:
    result = Div({"foo": "a"}, foo="b")
    assert str(result) == """<div foo="b"></div>"""


@pytest.mark.parametrize("not_an_attr", [1234, b"foo", object(), object, 1, 0, None])
def test_invalid_attribute_key(not_an_attr: t.Any) -> None:
    with pytest.raises(ValueError):
        str(Div({not_an_attr: "foo"}))


@pytest.mark.parametrize(
    "not_an_attr",
    [12.34, b"foo", object(), object],
)
def test_invalid_attribute_value(not_an_attr: t.Any) -> None:
    with pytest.raises(ValueError):
        Div(foo=not_an_attr)
