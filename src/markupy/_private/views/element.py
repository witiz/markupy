from collections.abc import Iterator, Mapping
from functools import lru_cache
from re import match as re_fullmatch
from re import sub as re_sub
from typing import Any, TypeAlias, overload

from typing_extensions import Self, override

from markupy.exceptions import MarkupyError

from ..attributes import Attribute, AttributeStore
from .fragment import Fragment

AttributeArgs: TypeAlias = (
    Mapping[Attribute.Name, Attribute.Value]
    | tuple[Attribute.Name, Attribute.Value]
    | Attribute
    | None
)


class Element(Fragment):
    __slots__ = ("_attributes", "_name")

    def __init__(self, name: str, *, safe: bool = False, shared: bool = True) -> None:
        super().__init__(safe=safe, shared=shared)
        self._name = name
        self._attributes: str | None = None

    def __copy__(self) -> Self:
        return type(self)(self.name, shared=False)

    @property
    def name(self) -> str:
        return self._name

    def _tag_opening(self) -> str:
        if attributes := self._attributes:
            return f"<{self._name} {attributes}>"
        return f"<{self._name}>"

    def _tag_closing(self) -> str:
        return f"</{self._name}>"

    def __iter__(self) -> Iterator[str]:
        yield self._tag_opening()
        yield from super().__iter__()
        yield self._tag_closing()

    def __repr__(self) -> str:
        return f"<markupy.{type(self).__name__}.{self._name}>"

    # Use call syntax () to define attributes
    @overload
    def __call__(self, *args: AttributeArgs, **kwargs: Attribute.Value) -> Self: ...
    @overload
    def __call__(
        self,
        selector: str,
        *args: AttributeArgs,
        **kwargs: Attribute.Value,
    ) -> Self: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Self:
        if self._attributes is not None:
            raise MarkupyError(
                f"Illegal attempt to redefine attributes for element {self!r}"
            )

        if self._children:
            raise MarkupyError(
                f"Illegal attempt to define attributes after children for element {self!r}"
            )

        attrs = AttributeStore()
        for arg in args:
            if len(attrs) == 0 and isinstance(arg, str):
                attrs.add_selector(arg)
            elif arg is None:
                pass
            elif isinstance(arg, Mapping):
                attrs.add_dict(arg)  # type:ignore[unused-ignore]
            elif isinstance(arg, tuple):
                attrs.add_tuple(arg)  # type:ignore[unused-ignore]
            elif isinstance(arg, Attribute):
                attrs.add(arg)
            else:
                raise MarkupyError(f"Invalid argument {arg!r} for element {self!r}")
        if kwargs:
            attrs.add_dict(kwargs, rewrite_keys=True)

        if attributes := str(attrs):
            el = self._get_instance()
            el._attributes = attributes
            return el

        return self


class HtmlElement(Element):
    __slots__ = ()

    @override
    def __iter__(self) -> Iterator[str]:
        yield "<!doctype html>"
        yield from super().__iter__()


class VoidElement(Element):
    __slots__ = ()

    @override
    def __iter__(self) -> Iterator[str]:
        yield self._tag_opening()

    @override
    def __getitem__(self, children: Any) -> Self:
        raise MarkupyError(f"Void element {self!r} cannot contain children")


class CommentElement(Element):
    __slots__ = ()

    @override
    def _tag_opening(self) -> str:
        return "<!--"

    @override
    def _tag_closing(self) -> str:
        return "-->"

    @override
    def __call__(self, *args: Any, **kwargs: Any) -> Self:
        raise MarkupyError(f"Comment element {self!r} cannot have attributes")


class SafeElement(Element):
    __slots__ = ()

    def __init__(self, name: str, *, shared: bool = True) -> None:
        super().__init__(name, safe=True, shared=shared)


SPECIAL_ELEMENTS: dict[str, type[Element]] = {
    "area": VoidElement,
    "base": VoidElement,
    "br": VoidElement,
    "col": VoidElement,
    "embed": VoidElement,
    "hr": VoidElement,
    "img": VoidElement,
    "input": VoidElement,
    "link": VoidElement,
    "meta": VoidElement,
    "param": VoidElement,
    "source": VoidElement,
    "track": VoidElement,
    "wbr": VoidElement,
    "_": CommentElement,
    "script": SafeElement,
    "style": SafeElement,
    "html": HtmlElement,
}


@lru_cache(maxsize=300)
def get_element(name: str) -> Element:
    if name == "_":
        # Special exception for CommentElement
        html_name = "_"
    elif name.startswith("_"):
        # Needed when called from __getattr__
        raise AttributeError
    elif not re_fullmatch(r"^(?:[A-Z][a-z0-9]*)+$", name):
        raise MarkupyError(
            f"`{name}` is not a valid element name (must use CapitalizedCase)"
        )
    else:
        # Uppercase chars are word boundaries for tag names
        words = filter(None, re_sub(r"([A-Z])", r" \1", name).split())
        html_name = "-".join(words).lower()

    cls = SPECIAL_ELEMENTS.get(html_name, Element)
    return cls(html_name)
