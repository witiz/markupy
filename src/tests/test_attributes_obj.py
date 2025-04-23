from markupy import attributes as attr
from markupy import elements as el


def test_int() -> None:
    result = """<input minlength="0" maxlength="5">"""
    assert el.Input(attr.minlength(0), attr.maxlength(5)) == result


def test_boolean() -> None:
    result = """<input disabled>"""
    assert el.Input(attr.disabled()) == result
    assert el.Input(attr.disabled(True)) == result


def test_missing_attribute() -> None:
    result = """<h1 foo-bar="baz"></h1>"""
    assert el.H1(attr.foo_bar("baz")) == result


def test_classes() -> None:
    result = """<h1 class="foo bar"></h1>"""
    assert el.H1(attr.class_("foo bar")) == result


def test_class_list() -> None:
    result = """<h1 class="foo bar"></h1>"""
    assert el.H1(attr.class_(["foo", "bar"])) == result


def test_class_dict() -> None:
    result = """<h1 class="foo bar"></h1>"""
    assert el.H1(attr.class_({"foo": True, "baz": False, "bar": True})) == result


def test_non_identifier() -> None:
    result = """<input @click="hello">"""
    assert el.Input(attr._("@click", "hello")) == result
