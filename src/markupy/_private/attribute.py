from collections.abc import Iterator, Mapping
from functools import lru_cache
from typing import Any, Callable, TypeAlias

from markupsafe import escape

from ..exceptions import MarkupyError

AttributeValue: TypeAlias = None | bool | str | int | float


class Attribute:
    __slots__ = ("name", "value")

    def __init__(self, name: str, value: AttributeValue):
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"<markupy.Attribute.{self.name}>"


AttributeHandler: TypeAlias = Callable[[Attribute | None, Attribute], Attribute | None]


class AttributeHandlerRegistry:
    def __init__(self) -> None:
        self._handlers: dict[AttributeHandler, None] = dict()

    def register(self, handler: AttributeHandler) -> AttributeHandler:
        """Registers the handler and returns it unchanged (so usable as a decorator)."""
        if handler in self._handlers:
            raise ValueError(f"Handler {handler.__name__} is already registered.")
        self._handlers[handler] = None
        return handler  # Important for decorator usage

    def unregister(self, handler: AttributeHandler) -> None:
        self._handlers.pop(handler, None)

    def __iter__(self) -> Iterator[AttributeHandler]:
        yield from reversed(self._handlers.keys())


attribute_handlers = AttributeHandlerRegistry()


@attribute_handlers.register
def default_attribute_handler(
    old: Attribute | None, new: Attribute
) -> Attribute | None:
    if old is None:
        return new
    elif new.name == "class":
        # For class, append new values
        new.value = f"{old.value} {new.value}"
        return new
    else:
        raise MarkupyError(f"Invalid attempt to redefine attribute `{new.name}`")


@lru_cache(maxsize=1000)
def python_to_html_key(key: str) -> str:
    if not key.isidentifier():
        # Might happen when using the **{} syntax
        raise MarkupyError(f"Attribute `{key}` has invalid name")
    if key == "_":
        # Preserve single underscore for hyperscript compatibility
        return key
    # Trailing underscore "_" is meaningless and is used to escape protected
    # keywords that might be used as attr keys such as class_ and for_
    # Underscores become dashes
    return key.removesuffix("_").replace("_", "-")


@lru_cache(maxsize=1000)
def is_valid_key(key: Any) -> bool:
    # Check for invalid chars (like <>, newline/spaces, upper case)
    return bool(
        key != "" and key == escape(str(key)) and key == "".join(key.lower().split())
    )


def is_valid_value(value: Any) -> bool:
    return isinstance(value, AttributeValue)


def format_key_value(key: str, value: AttributeValue) -> str | None:
    if (
        value is None
        or value is False
        or (value == "" and key in {"id", "class", "name"})
    ):
        # Discard False and None valued attributes for all attributes
        # Discard empty id, class, name attributes
        return None
    elif value is True:
        return key
    return f'{key}="{escape(str(value))}"'


class AttributeDict(dict[str, AttributeValue]):
    __slots__ = ()

    def __setitem__(self, key: str, value: AttributeValue) -> None:
        if not is_valid_key(key):
            raise MarkupyError(f"Attribute `{key!r}` has invalid name")

        if not is_valid_value(value):
            raise MarkupyError(f"Attribute `{key}` has invalid value {value!r}")

        return super().__setitem__(key, value)

    def __str__(self) -> str:
        values = [format_key_value(k, v) for k, v in self.items()]
        return " ".join(filter(None, values))

    def add_selector(self, selector: str) -> None:
        if selector := selector.replace(".", " ").strip():
            if "#" in selector[1:]:
                raise MarkupyError(
                    "Id must be defined only once and must be in first position of selector"
                )
            if selector.startswith("#"):
                id, *classes = selector.split()
                self.set_attribute(Attribute("id", id[1:]))
            else:
                classes = selector.split()

            self.set_attribute(Attribute("class", " ".join(classes)))

    def add_dict(
        self,
        dct: Mapping[str, AttributeValue],
        *,
        rewrite_keys: bool = False,
    ) -> None:
        for key, value in dct.items():
            name = python_to_html_key(key) if rewrite_keys else key
            self.set_attribute(Attribute(name, value))

    def add_objs(self, lst: list[Attribute]) -> None:
        for attr in lst:
            self.set_attribute(attr)

    def set_attribute(self, new: Attribute) -> None:
        key = new.name
        old = Attribute(key, self[key]) if key in self else None
        for handler in attribute_handlers:
            if attribute := handler(old, new):
                # Use attribute.name here to allow for key rewrite
                self[attribute.name] = attribute.value
                return
