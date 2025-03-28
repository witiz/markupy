from collections.abc import Iterator
from typing import Any, overload

from typing_extensions import Self, override

from .attribute import AttributeDict, AttributeValue
from .fragment import Fragment
from .node import iter_node


class Element(Fragment):
    __slots__ = ("_name", "_attributes")

    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name
        self._attributes: str | None = None

    def __copy__(self) -> Self:
        return type(self)(self.name)

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
        yield from iter_node(self._children, safe=self._safe)
        yield self._tag_closing()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self._tag_opening()}'>"

    # Use call syntax () to define attributes
    @overload
    def __call__(
        self,
        selector: str,
        attributes: dict[str, AttributeValue],
        **kwargs: AttributeValue,
    ) -> Self: ...
    @overload
    def __call__(self, selector: str, **kwargs: AttributeValue) -> Self: ...
    @overload
    def __call__(
        self, attributes: dict[str, AttributeValue], **kwargs: AttributeValue
    ) -> Self: ...
    @overload
    def __call__(self, **kwargs: AttributeValue) -> Self: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Self:
        selector: str | None = None
        attributes_dict: dict[str, AttributeValue] | None = None
        attributes_kwargs: dict[str, AttributeValue] = kwargs
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                # element(".foo")
                selector = arg
            elif isinstance(arg, dict):
                # element({"foo": "bar"})
                attributes_dict = arg
            else:
                raise TypeError(
                    f"Invalid argument type `{arg!r}` for element {self}, expected `str` or `dict`"
                )
        elif len(args) == 2:
            # element(".foo", {"bar": "baz"})
            if not isinstance(args[0], str):
                raise TypeError(
                    f"Invalid first argument type `{args[0]!r}` for element {self}, expected `str`"
                )
            if not isinstance(args[1], dict):
                raise TypeError(
                    f"Invalid second argument type `{args[1]!r}` for element {self}, expected `dict`"
                )
            selector, attributes_dict = args
        elif len(args) > 2:
            raise ValueError(f"Invalid number of arguments provided for element {self}")

        if not selector and not attributes_dict and not attributes_kwargs:
            return self

        attrs = AttributeDict()
        try:
            attrs.add_selector(selector)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid selector string `{selector}` for element {self}")
        try:
            attrs.add_dict(attributes_dict)
        except (TypeError, ValueError):
            raise ValueError(
                f"Invalid dict attributes `{attributes_dict}` for element {self}"
            )
        try:
            attrs.add_dict(attributes_kwargs, rewrite_keys=True)
        except (TypeError, ValueError):
            raise ValueError(
                f"Invalid keyword attributes `{attributes_kwargs}` for element {self}"
            )

        if attributes := str(attrs):
            el = self._new_instance()
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
        raise ValueError(f"Void element {self} cannot contain children")


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
        raise ValueError(f"Comment element {self} cannot have attributes")


class SafeElement(Element):
    __slots__ = ()

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._safe = True
