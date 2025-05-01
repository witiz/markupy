from functools import lru_cache
from typing import Any

from markupsafe import escape

from markupy.exceptions import MarkupyError

AttributeValue = None | bool | str | int | float


@lru_cache(maxsize=1000)
def is_valid_key(key: Any) -> bool:
    # Check for invalid chars (like <>, newline/spaces, upper case)
    return (
        isinstance(key, str)
        and key != ""
        # ensure no special chars
        and key == escape(str(key))
        # ensure no newlines/spaces/tabs and lowercase
        and key == "".join(key.lower().split())
    )


def is_valid_value(value: Any) -> bool:
    return isinstance(value, AttributeValue)


class Attribute:
    __slots__ = ("_name", "_value")

    _name: str
    _value: AttributeValue

    def __init__(self, name: str, value: AttributeValue) -> None:
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
            return ""
        elif self.value is True:
            return self.name
        return f'{self.name}="{escape(str(self.value))}"'

    def __repr__(self) -> str:
        return f"<markupy.Attribute.{self.name}>"
