from collections.abc import Iterator, Mapping
from functools import lru_cache
from typing import Any, Callable, TypeAlias

from markupsafe import escape

from ..exceptions import MarkupyError

AttributeValue: TypeAlias = None | bool | str | int | float


@lru_cache(maxsize=1000)
def is_valid_key(key: Any) -> bool:
    # Check for invalid chars (like <>, newline/spaces, upper case)
    return bool(
        key != "" and key == escape(str(key)) and key == "".join(key.lower().split())
    )


def is_valid_value(value: Any) -> bool:
    return isinstance(value, AttributeValue)


class Attribute:
    __slots__ = ("_name", "_value")

    _name: str
    _value: AttributeValue

    def __init__(self, name: str, value: AttributeValue) -> None:
        self.name = name
        self.value = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if not is_valid_key(name):
            raise MarkupyError(f"Attribute `{name!r}` has invalid name")
        self._name = name

    @property
    def value(self) -> AttributeValue:
        return self._value

    @value.setter
    def value(self, value: AttributeValue) -> None:
        if not is_valid_value(value):
            raise MarkupyError(f"Attribute `{self.name}` has invalid value {value!r}")
        self._value = value

    def __str__(self) -> str:
        if self.value is None or self.value is False:
            # Discard False and None valued attributes for all attributes
            # Discard empty id, class, name attributes
            return ""
        elif self.value is True:
            return self.name
        return f'{self.name}="{escape(str(self.value))}"'

    def __repr__(self) -> str:
        return f"<markupy.Attribute.{self.name}>"


# We prefer this signature over (name:str, old_value:AttributeValue, new_value:AttributeValue)
# for several reasons:
# - avoid exposing AttributeValue type that is too low level
# - allows to differentiate between an attribute that have never been instanciated vs
#   an attribute that has already been instanciated with a None value
AttributeHandler: TypeAlias = Callable[[Attribute | None, Attribute], Attribute | None]


class AttributeHandlerRegistry(dict[AttributeHandler, None]):
    def register(self, handler: AttributeHandler) -> AttributeHandler:
        """Registers the handler and returns it unchanged (so usable as a decorator)."""
        if handler in self:
            raise ValueError(f"Handler {handler.__name__} is already registered.")
        self[handler] = None
        return handler  # Important for decorator usage

    def unregister(self, handler: AttributeHandler) -> None:
        self.pop(handler, None)

    def __iter__(self) -> Iterator[AttributeHandler]:
        yield from reversed(self.keys())


attribute_handlers = AttributeHandlerRegistry()


@attribute_handlers.register
def default_attribute_handler(
    old: Attribute | None, new: Attribute
) -> Attribute | None:
    if old is None or old.value is None:
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


class Attributes(dict[str, Attribute]):
    __slots__ = ()

    def __setitem__(self, key: str, new: Attribute) -> None:
        old = self[key] if key in self else None
        for handler in attribute_handlers:
            if attribute := handler(old, new):
                # Use attribute.name here to allow for key rewrite
                key = attribute.name
                new = attribute
                break

        super().__setitem__(key, new)

    def __str__(self) -> str:
        return " ".join(filter(None, map(str, self.values())))

    def add_selector(self, selector: str) -> None:
        if selector := selector.replace(".", " ").strip():
            if "#" in selector[1:]:
                raise MarkupyError(
                    "Id must be defined only once and must be in first position of selector"
                )
            if selector.startswith("#"):
                rawid, *classes = selector.split()
                if id := rawid[1:]:
                    self.add(Attribute("id", id))
            else:
                classes = selector.split()

            if classes:
                self.add(Attribute("class", " ".join(classes)))

    def add_dict(
        self,
        dct: Mapping[str, AttributeValue],
        *,
        rewrite_keys: bool = False,
    ) -> None:
        for key, value in dct.items():
            name = python_to_html_key(key) if rewrite_keys else key
            self.add(Attribute(name, value))

    def add_objs(self, lst: list[Attribute]) -> None:
        for attr in lst:
            self.add(attr)

    def add(self, new: Attribute) -> None:
        self[new.name] = new
