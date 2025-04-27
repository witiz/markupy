from collections.abc import Iterator, Mapping
from typing import Any, overload

from typing_extensions import Self, override

from ..exceptions import MarkupyError
from .attribute import Attribute, Attributes, AttributeValue
from .fragment import Fragment


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
    def __call__(self, *args: Attribute | None, **kwargs: AttributeValue) -> Self: ...
    @overload
    def __call__(
        self, selector: str, *args: Attribute | None, **kwargs: AttributeValue
    ) -> Self: ...
    @overload
    def __call__(
        self,
        attributes: Mapping[str, AttributeValue],
        *args: Attribute | None,
        **kwargs: AttributeValue,
    ) -> Self: ...
    @overload
    def __call__(
        self,
        selector: str,
        attributes: Mapping[str, AttributeValue],
        *args: Attribute | None,
        **kwargs: AttributeValue,
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

        has_selector = False
        has_dict = False
        has_obj = False

        attrs = Attributes()
        for arg in args:
            if not (has_selector or has_dict or has_obj) and isinstance(arg, str):
                has_selector = True
                attrs.add_selector(arg)
            elif not (has_dict or has_obj) and isinstance(arg, Mapping):
                has_dict = True
                attrs.add_dict(arg)  # type:ignore[unused-ignore]
            elif arg is None:
                has_obj = True
            elif isinstance(arg, Attribute):
                has_obj = True
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
