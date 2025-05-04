import markupy.attributes as at
import markupy.elements as el
from markupy import Attribute


def test_int() -> None:
    result = """<input minlength="0" maxlength="5">"""
    assert el.Input(at.minlength(0), at.maxlength(5)) == result


def test_boolean() -> None:
    result = """<input disabled>"""
    assert el.Input(at.disabled()) == result
    assert el.Input(at.disabled(True)) == result


def test_missing_attribute() -> None:
    result = """<h1 foo-bar="baz"></h1>"""
    assert el.H1(at.foo_bar("baz")) == result


def test_classes() -> None:
    result = """<h1 class="foo bar"></h1>"""
    assert el.H1(at.class_("foo bar")) == result


def test_class_list() -> None:
    result = """<h1 class="foo bar"></h1>"""
    assert el.H1(at.class_(["foo", "bar"])) == result


def test_class_dict() -> None:
    result = """<h1 class="foo bar"></h1>"""
    assert el.H1(at.class_({"foo": True, "baz": False, "bar": True})) == result


def test_non_identifier() -> None:
    result = """<input @click="hello">"""
    assert el.Input(Attribute("@click", "hello")) == result


def test_none() -> None:
    assert el.Input(None) == """<input>"""
    assert el.Input("#foo", None) == """<input id="foo">"""
    assert el.Input(at.foo("bar"), None) == """<input foo="bar">"""
    assert el.Input(None, at.foo("bar")) == """<input foo="bar">"""
    assert el.Input(None, foo="bar") == """<input foo="bar">"""
