from collections.abc import Mapping
from functools import lru_cache
from typing import TypeAlias

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


def format_key_value(key: str, value: AttributeValue) -> str:
    if value is True:
        return key
    return f'{key}="{escape(str(value))}"'


class AttributeDict(dict[str, AttributeValue]):
    __slots__ = ()

    def __setitem__(self, key: str, value: AttributeValue) -> None:
        key = key.lower()
        if (
            value is None
            or value is False
            or (value == "" and key in {"id", "class", "name"})
        ):
            # Discard False and None valued attributes for all attributes
            # Discard empty id, class, name attributes
            return

        if key == "class":
            if current := self.get(key):
                # For class, append new values instead of replacing them
                value = f"{current} {value}"

        return super().__setitem__(key, value)

    def __str__(self) -> str:
        return " ".join(format_key_value(k, v) for k, v in self.items())

    def add_selector(self, selector: str) -> None:
        if selector := selector.replace(".", " ").strip():
            if "#" in selector[1:]:
                raise MarkupyError(
                    "Id must be defined only once and must be in first position of selector"
                )
            if selector.startswith("#"):
                id, *classes = selector.split()
                self["id"] = id[1:]
                self["class"] = " ".join(classes)
            else:
                classes = selector.split()
                self["class"] = " ".join(classes)

    def add_dict(
        self,
        dct: Mapping[str, AttributeValue],
        *,
        rewrite_keys: bool = False,
    ) -> None:
        for key, value in dct.items():
            if not isinstance(value, AttributeValue):  # type: ignore[unused-ignore]
                raise MarkupyError(
                    f"Invalid value type {value!r} for attribute `{key}`"
                )

            if rewrite_keys:
                key = python_to_html_key(key)
            else:
                # Coming from dict arg, need to secure user input
                if not isinstance(key, str):  # pyright: ignore [reportUnnecessaryIsInstance]
                    raise MarkupyError(f"Attribute {key!r} must be a string")
                if escape(str(key)) != key or len(key.split()) > 1:
                    raise MarkupyError(f"Attribute `{key}` has invalid name")

            self[key] = value

    def add_objs(self, lst: list[Attribute]) -> None:
        for attr in lst:
            self[attr.name] = attr.value
