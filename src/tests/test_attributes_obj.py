from markupy import attributes as attr
from markupy import elements as el


def test_int() -> None:
    result = """<input minlength="0" maxlength="5">"""
    assert str(el.Input(attr.minlength(0), attr.maxlength(5))) == result


def test_boolean() -> None:
    result = """<input disabled>"""
    assert str(el.Input(attr.disabled())) == result
    assert str(el.Input(attr.disabled(True))) == result


def test_element_attribute() -> None:
    result = """<meta http-equiv="refresh">"""
    assert str(el.Meta(attr.Meta.http_equiv("refresh"))) == result


def test_classes() -> None:
    result = """<h1 class="foo bar"></h1>"""
    assert str(el.H1(attr.class_("foo", "bar"))) == result


def test_class_list() -> None:
    result = """<h1 class="foo bar"></h1>"""
    assert str(el.H1(attr.class_list(["foo", "bar"]))) == result


def test_class_dict() -> None:
    result = """<h1 class="foo bar"></h1>"""
    assert (
        str(el.H1(attr.class_dict({"foo": True, "baz": False, "bar": True}))) == result
    )
