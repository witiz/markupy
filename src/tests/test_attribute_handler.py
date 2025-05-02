from contextlib import contextmanager
from typing import Generator

import pytest

from markupy import Attribute, attribute_handlers
from markupy import elements as el
from markupy._private.attributes.handlers import AttributeHandler
from markupy.exceptions import MarkupyError


@contextmanager
def tmp_handler(handler: AttributeHandler) -> Generator[None, None, None]:
    """Temporarily register a handler within a context."""
    attribute_handlers.register(handler)
    try:
        yield
    finally:
        attribute_handlers.unregister(handler)
    return None


def test_multi_register() -> None:
    def handler(old: Attribute | None, new: Attribute) -> Attribute | None:
        return None

    with tmp_handler(handler):
        with pytest.raises(MarkupyError):
            attribute_handlers.register(handler)


def test_handler_order() -> None:
    def handler1(old: Attribute | None, new: Attribute) -> Attribute | None:
        new.value = f"{new.value}1"
        return None

    def handler2(old: Attribute | None, new: Attribute) -> Attribute | None:
        new.value = f"{new.value}2"
        return None

    with tmp_handler(handler1):
        with tmp_handler(handler2):
            assert el.Input(foo="bar") == """<input foo="bar21">"""


def test_handler() -> None:
    def handler(old: Attribute | None, new: Attribute) -> Attribute | None:
        if new.name == "id":
            assert old is None and new.value == "foo"
        elif new.name == "class":
            assert (old is None and new.value == "bar") or (
                old is not None and old.value == "bar" and new.value == "baz"
            )
        elif new.name == "hello":
            assert old is None and new.value == "world"
        else:
            raise Exception("Not supposed to happen")
        return None

    with tmp_handler(handler):
        el.Input("#foo.bar", class_="baz", hello="world")


def test_class_replace() -> None:
    def handler(old: Attribute | None, new: Attribute) -> Attribute | None:
        if new.name == "class":
            return new
        return None

    with tmp_handler(handler):
        assert el.Input(".foo", class_="bar") == """<input class="bar">"""


def test_prefix_attribute() -> None:
    def handler(old: Attribute | None, new: Attribute) -> Attribute | None:
        prefix = "foo-"
        if not new.name.startswith(prefix):
            return Attribute(f"{prefix}{new.name}", new.value)
        return None

    with tmp_handler(handler):
        assert (
            el.Input("#bar.baz", hello="world")
            == """<input foo-id="bar" foo-class="baz" foo-hello="world">"""
        )
