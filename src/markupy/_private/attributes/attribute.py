from functools import lru_cache
from typing import Any, TypeAlias

from markupsafe import escape

from markupy.exceptions import MarkupyError


@lru_cache(maxsize=1000)
def is_valid_key(key: Any) -> bool:
    # Check for invalid chars (like <>, newline/spaces, upper case)
    return (
        isinstance(key, Attribute.Name)
        and key != ""
        # ensure no special chars
        and key == escape(str(key))
        # ensure no newlines/spaces/tabs and lowercase
        and key == "".join(key.lower().split())
    )


def is_valid_value(value: Any) -> bool:
    return isinstance(value, Attribute.Value)


class Attribute:
    __slots__ = ("_name", "_value")

    Name: TypeAlias = str
    Value: TypeAlias = None | bool | str | int | float
    _name: Name
    _value: Value

    def __init__(self, name: str, value: Value) -> None:
        # name is immutable
        # reason is to avoid, when a handler returns None, having following handlers
        # receiving old and new instances with different names
        if not is_valid_key(name):
            raise MarkupyError(f"Attribute `{name!r}` has invalid name")
        self._name = name
        # value is mutable
        self.value = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> Value:
        return self._value

    @value.setter
    def value(self, value: Value) -> None:
        if not is_valid_value(value):
            raise MarkupyError(f"Attribute `{self.name}` has invalid value {value!r}")
        self._value = value

    def __str__(self) -> str:
        if self.value is None or self.value is False:
            # Discard False and None valued attributes for all attributes
            return ""
        elif self.value is True:
            return self.name
        return f'{self.name}="{escape(str(self.value))}"'

    def __repr__(self) -> str:
        return f"<markupy.Attribute.{self.name}>"
