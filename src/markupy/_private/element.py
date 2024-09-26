from collections.abc import Iterator
from typing import Any, overload

from typing_extensions import Self, override

from .attribute import AttributeDict, AttributeValue
from .view import Node, View, iter_node, validate_node


class Element(View):
    def __init__(self, name: str) -> None:
        self._name = name
        self._attributes: AttributeDict | None = None
        self._children: Node = None

    @property
    def name(self) -> str:
        return self._name

    def _tag_opening(self) -> str:
        if attributes := self._attributes:
            attributes_str = str(attributes)
            if len(attributes_str) > 0:
                return f"<{self._name} {attributes_str}>"
        return f"<{self._name}>"

    def _tag_closing(self) -> str:
        return f"</{self._name}>"

    def __iter__(self) -> Iterator[str]:
        yield self._tag_opening()
        yield from iter_node(self._children)
        yield self._tag_closing()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self._tag_opening()}'>"

    def _new_instance(self: Self) -> Self:
        # When imported, elements are loaded from a shared instance
        # Make sure we re-instantiate them on setting attributes/children
        # to avoid sharing attributes/children between multiple instances
        if self._attributes is None and self._children is None:
            return self.__class__(self._name)
        return self

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

        attributes = AttributeDict()
        try:
            attributes.add_selector(selector)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid selector string `{selector}` for element {self}")
        try:
            attributes.add_dict(attributes_dict)
        except (TypeError, ValueError):
            raise ValueError(
                f"Invalid dict attributes `{attributes_dict}` for element {self}"
            )
        try:
            attributes.add_dict(attributes_kwargs, rewrite_keys=True)
        except (TypeError, ValueError):
            raise ValueError(
                f"Invalid keyword attributes `{attributes_kwargs}` for element {self}"
            )

        if len(attributes) == 0:
            return self

        el = self._new_instance()
        el._attributes = attributes
        return el

    # Use subscriptable [] syntax to assign children
    def __getitem__(self, children: "Node") -> Self:
        if not validate_node(children):
            return self

        el = self._new_instance()
        el._children = children
        return el

    # Allow starlette Response.render to directly render this element without
    # explicitly casting to str:
    # https://github.com/encode/starlette/blob/5ed55c441126687106109a3f5e051176f88cd3e6/starlette/responses.py#L44-L49
    def encode(self, encoding: str = "utf-8", errors: str = "strict") -> bytes:
        return str(self).encode(encoding, errors)

    # Avoid having Django "call" a markupy element that is injected into a
    # template. Setting do_not_call_in_templates will prevent Django from doing
    # an extra call:
    # https://docs.djangoproject.com/en/5.0/ref/templates/api/#variables-and-lookups
    do_not_call_in_templates = True


class HtmlElement(Element):
    @override
    def __iter__(self) -> Iterator[str]:
        yield "<!doctype html>"
        yield from super().__iter__()


class VoidElement(Element):
    @override
    def __iter__(self) -> Iterator[str]:
        yield self._tag_opening()

    @override
    def __getitem__(self, children: Any) -> Self:
        raise ValueError(f"Void element {self} cannot contain children")


class CommentElement(Element):
    @override
    def _tag_opening(self) -> str:
        return "<!--"

    @override
    def _tag_closing(self) -> str:
        return "-->"

    @override
    def __call__(self, *args: Any, **kwargs: Any) -> Self:
        raise ValueError(f"Comment element {self} cannot have attributes")
