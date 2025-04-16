from collections.abc import Iterator, Mapping
from typing import Any, overload

from typing_extensions import Self, override

from ..exception import MarkupyError
from .attribute import AttributeDict, AttributeValue
from .shared import Shared


class Element(Shared):
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
    def __call__(
        self,
        selector: str,
        attributes: Mapping[str, AttributeValue],
        **kwargs: AttributeValue,
    ) -> Self: ...
    @overload
    def __call__(self, selector: str, **kwargs: AttributeValue) -> Self: ...
    @overload
    def __call__(
        self, attributes: Mapping[str, AttributeValue], **kwargs: AttributeValue
    ) -> Self: ...
    @overload
    def __call__(self, **kwargs: AttributeValue) -> Self: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Self:
        if self._attributes is not None:
            raise MarkupyError(
                f"Illegal attempt to redefine attributes for element {self!r}"
            )

        if self._children:
            raise MarkupyError(
                f"Illegal attempt to define attributes after children for element {self!r}"
            )

        selector: str | None = None
        attributes_dict: Mapping[str, AttributeValue] | None = None
        attributes_kwargs: Mapping[str, AttributeValue] = kwargs
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                # element(".foo")
                selector = arg
            elif isinstance(arg, Mapping):
                # element({"foo": "bar"})
                attributes_dict = arg  # type:ignore[unused-ignore]
            else:
                raise MarkupyError(
                    f"Invalid argument type {arg!r} for element {self!r}, expected `str` or `Mapping`"
                )
        elif len(args) == 2:
            # element(".foo", {"bar": "baz"})
            if not isinstance(args[0], str):
                raise MarkupyError(
                    f"Invalid first argument type {args[0]!r} for element {self!r}, expected `str`"
                )
            if not isinstance(args[1], Mapping):
                raise MarkupyError(
                    f"Invalid second argument type {args[1]!r} for element {self!r}, expected `Mapping`"
                )
            selector, attributes_dict = args
        elif len(args) > 2:
            raise MarkupyError(
                f"Invalid number of arguments provided for element {self!r}"
            )

        if not selector and not attributes_dict and not attributes_kwargs:
            return self

        attrs = AttributeDict()
        try:
            attrs.add_selector(selector)
        except Exception as e:
            raise MarkupyError(
                f"Invalid selector string `{selector}` for element {self!r}"
            ) from e
        try:
            attrs.add_dict(attributes_dict)
        except Exception as e:
            raise MarkupyError(
                f"Invalid dict attributes `{attributes_dict}` for element {self!r}"
            ) from e
        try:
            attrs.add_dict(attributes_kwargs, rewrite_keys=True)
        except Exception as e:
            raise MarkupyError(
                f"Invalid keyword attributes `{attributes_kwargs}` for element {self!r}"
            ) from e

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
