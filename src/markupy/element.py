from collections.abc import Callable, Iterable, Iterator
from functools import lru_cache
from re import sub as re_sub
from typing import Any, TypeAlias, overload

from markupsafe import Markup, escape
from typing_extensions import Self, override

from .attribute import AttributeDict, AttributeValue


def is_void_element(name: str) -> bool:
    return name in {
        "area",
        "base",
        "br",
        "col",
        "command",
        "embed",
        "hr",
        "img",
        "input",
        "keygen",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }


class Element:
    def __init__(self, name: str) -> None:
        self.name = name
        self.attributes: AttributeDict | None = None
        self.children: Node = None

    def tag_opening(self) -> str:
        if attributes := self.attributes:
            attributes_str = str(attributes)
            if len(attributes_str) > 0:
                return f"<{self.name} {attributes_str}>"
        return f"<{self.name}>"

    def tag_closing(self) -> str:
        return f"</{self.name}>"

    def __iter__(self) -> Iterator[str]:
        yield self.tag_opening()
        yield from iter_node(self.children)
        yield self.tag_closing()

    def __str__(self) -> str:
        return Markup("".join(self))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.tag_opening()}'>"

    @staticmethod
    @lru_cache(maxsize=300)
    def shared_instance(name: str) -> "Element":
        if set(name) == {"_"}:
            return CommentElement(name)

        # Consider uppercase chars and underscores as word boundaries for tag names
        words = filter(None, re_sub(r"([A-Z])", r"_\1", name).split("_"))
        html_name = "-".join(words).lower()
        if html_name == "html":
            return HtmlElement(html_name)
        elif is_void_element(html_name):
            return VoidElement(html_name)
        else:
            return Element(html_name)

    def unshared_instance(self: Self) -> Self:
        # When imported, elements are loaded from cache
        # Make sure we re-instantiate them on setting attributes/children
        # to avoid sharing attributes/children between multiple instances
        if self.attributes is None and self.children is None:
            return self.__class__(self.name)
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

        el = self.unshared_instance()
        el.attributes = attributes
        return el

    # Use subscriptable [] syntax to assign children
    def __getitem__(self, children: "Node") -> Self:
        el = self.unshared_instance()
        el.children = children
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
        yield self.tag_opening()

    @override
    def __getitem__(self, children: Any) -> Self:
        raise ValueError(f"Void element {self} cannot contain children")


class CommentElement(Element):
    @override
    def tag_opening(self) -> str:
        return "<!--"

    @override
    def tag_closing(self) -> str:
        return "-->"

    @override
    def __call__(self, *args: Any, **kwargs: Any) -> Self:
        raise ValueError(f"Comment element {self} cannot have attributes")


Node: TypeAlias = (
    None | bool | str | int | Element | Iterable["Node"] | Callable[[], "Node"]
)


def render_node(node: Node) -> Markup:
    return Markup("".join(iter_node(node)))


def iter_node(node: Node) -> Iterator[str]:
    if node is None or isinstance(node, bool):
        return
    while not isinstance(node, Element) and callable(node):
        node = node()
    if isinstance(node, Element):
        yield from node
    elif isinstance(node, int):
        yield str(node)
    elif isinstance(node, str):
        yield str(escape(node))
    elif isinstance(node, Iterable):
        for child in node:
            yield from iter_node(child)
    else:
        raise TypeError(f"{node!r} is not a valid child element")
