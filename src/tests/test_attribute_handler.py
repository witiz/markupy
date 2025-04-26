from contextlib import contextmanager
from typing import Generator

from markupy import Attribute, attribute_handlers
from markupy import elements as el
from markupy._private.attribute import AttributeHandler


@contextmanager
def tmp_handler(handler: AttributeHandler) -> Generator[None, None, None]:
    """Temporarily register a handler within a context."""
    attribute_handlers.register(handler)
    try:
        yield
    finally:
        attribute_handlers.unregister(handler)
    return None


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
        new.name = f"foo-{new.name}"
        return new

    with tmp_handler(handler):
        assert (
            el.Input("#bar.baz", hello="world")
            == """<input foo-id="bar" foo-class="baz" foo-hello="world">"""
        )
