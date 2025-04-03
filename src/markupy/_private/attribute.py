from collections.abc import Iterable, Iterator, Mapping, Sequence
from functools import lru_cache
from re import match as re_match
from re import sub as re_sub
from typing import TypeAlias

from markupsafe import escape

from ..exception import MarkupyError

ClassNamesDict: TypeAlias = Mapping[str, bool | None]
ClassNamesSequence: TypeAlias = Sequence[None | str | ClassNamesDict]
ClassAttributeValue: TypeAlias = ClassNamesSequence | ClassNamesDict
OtherAttributeValue: TypeAlias = None | bool | str | int
AttributeValue: TypeAlias = OtherAttributeValue | ClassAttributeValue

# https://html.spec.whatwg.org/multipage/indices.html#attributes-3
BOOLEAN_ATTRIBUTES: set[str] = {
    "allowfullscreen",
    "async",
    "autofocus",
    "autoplay",
    "checked",
    "controls",
    "default",
    "defer",
    "disabled",
    "formnovalidate",
    "inert",
    "ismap",
    "itemscope",
    "loop",
    "multiple",
    "muted",
    "nomodule",
    "novalidate",
    "open",
    "playsinline",
    "readonly",
    "required",
    "reversed",
    "selected",
}


def _classes_to_str(classes: Iterable[str]) -> str:
    return " ".join(map(lambda c: c.strip(), filter(None, classes)))


def _iter_classes_dict(dct: ClassNamesDict) -> Iterator[str]:
    for k, v in dct.items():
        if v:
            yield k


def _iter_classes_seq(seq: ClassNamesSequence) -> Iterator[str]:
    for v in seq:
        if not v:
            continue
        if isinstance(v, Mapping):
            yield from _iter_classes_dict(v)
        else:
            yield v


@lru_cache(maxsize=1000)
def _rewrite_attr_key(key: str) -> str:
    # Leading underscore "_" not followed by another "_" -> "@"
    key = re_sub(r"^(?:_)([^_]+)", r"@\1", key)
    # Trailing underscore "_" is meaningless and is used to escape protected
    # keywords that might be used as attr keys such as class_ and for_
    key = key.removesuffix("_")
    # Upper case -> "-"
    key = "-".join(filter(None, re_sub(r"([A-Z])", r" \1", key).split())).lower()
    # Double underscore -> ":"
    key = key.replace("__", ":")
    # Single underscore -> "."
    key = key.replace("_", ".")
    return key


@lru_cache(maxsize=1000)
def is_boolean_attribute(name: str) -> bool:
    return name in BOOLEAN_ATTRIBUTES


def _format_key_value(key: str, value: AttributeValue) -> str:
    key_str: str = escape(str(key))
    if value is True:
        return key_str
    value_str: str = escape(str(value))
    return f'{key_str}="{value_str}"'


class AttributeDict(dict[str, AttributeValue]):
    def __setitem__(self, key: str, value: AttributeValue) -> None:
        if value is False or value is None:
            # Discard False and None valued attributes for all attributes
            return

        key = key.lower()
        if not re_match(r"^\S+$", key):
            raise MarkupyError(f"Attribute `{key}` has invalid name")

        if value is True:
            pass
        elif is_boolean_attribute(key):
            if isinstance(value, int) and not bool(value):
                return
            value = True
        elif value == "" and key in {"id", "class"}:
            # Discard empty id or class attributes
            return

        if key == "class" and self.get(key):
            return super().__setitem__(key, f"{self['class']} {value}")
        else:
            return super().__setitem__(key, value)

    def __str__(self) -> str:
        return " ".join(_format_key_value(k, v) for k, v in self.items())

    def add_selector(self, selector: str | None) -> None:
        if not selector:
            # Empty selector or None
            return

        selector = selector.replace(".", " ").strip()
        parts = selector.split()
        hash_indexes = [i for i, c in enumerate(selector) if c == "#"]

        if len(hash_indexes) > 1:
            raise MarkupyError("Id must be defined only once in selector")

        elif len(hash_indexes) == 1:
            if hash_indexes[0] != 0:
                raise MarkupyError("Id must be defined at the start of selector")

            if len(parts[0]) > 1:
                # If selector starts with '#id'
                self["id"] = parts[0][1:]
                self["class"] = _classes_to_str(parts[1:])
            elif len(parts) > 1:
                # If selector starts with '# id'
                self["id"] = parts[1]
                self["class"] = _classes_to_str(parts[2:])

        else:
            self["class"] = _classes_to_str(parts)

    def add_dict(
        self,
        dct: Mapping[str, AttributeValue] | None,
        *,
        rewrite_keys: bool = False,
    ) -> None:
        if not dct:
            # Empty dict or None
            return
        for key, value in dct.items():
            if not isinstance(key, str):  # pyright: ignore [reportUnnecessaryIsInstance]
                raise MarkupyError("Attribute key must be a string")

            if key != "_" and rewrite_keys:
                # Preserve single _ for hyperscript
                key = _rewrite_attr_key(key)

            if isinstance(value, OtherAttributeValue):
                self[key] = value
                continue

            elif key == "class":
                if isinstance(value, Mapping):
                    classes = _iter_classes_dict(value)
                else:
                    classes = _iter_classes_seq(value)
                self[key] = _classes_to_str(classes)
                continue

            raise MarkupyError(f"Invalid value type `{value!r}` for attribute `{key}`")
