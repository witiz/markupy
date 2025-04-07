from collections.abc import Iterable, Iterator
from typing import Any, final

from markupsafe import escape
from typing_extensions import Self

from ..exception import MarkupyError


def iter_node(node: Any) -> Iterator[tuple[Any, bool]]:
    if node is None or isinstance(node, bool):
        return
    elif isinstance(node, View):
        # View is Iterable, must check in priority
        yield node, True
    elif isinstance(node, Iterable) and not isinstance(node, str):
        for child in node:  # type: ignore[unused-ignore]
            yield from iter_node(child)
    else:
        yield node, False


class View(Iterable[str]):
    # Not using slots here so that subclasses can benefit from
    # auto-initialized instance vars without having to call super()
    _safe: bool = False
    _children: list["str | View"] | None = None

    def __init__(self, *, safe: bool = False) -> None:
        self._safe: bool = safe

    # Use subscriptable [] syntax to assign children
    def __getitem__(self, content: Any) -> Self:
        if self._children is not None:
            raise MarkupyError(f"Illegal attempt to redefine children of {self!r}")

        children: list[str | View] = list()
        for node, is_view in iter_node(content):
            if is_view:
                # Some View instances are callable, it must be checked in priority
                children.append(node)
            elif callable(node):
                # Allows to catch uncalled functions or uninstanciated classes
                raise MarkupyError(
                    f"Invalid child node {node!r} provided for {self!r}; Did you mean `{node.__name__}()` ?"
                )
            else:
                try:
                    if s := str(node if self._safe else escape(node)):
                        children.append(s)
                except Exception as e:
                    raise MarkupyError(
                        f"Invalid child node {node!r} provided for {self!r}"
                    ) from e

        if children:
            instance = self._get_instance()
            instance._children = children
            return instance

        return self

    def __iter__(self) -> Iterator[str]:
        if self._children:
            for node in self._children:
                if isinstance(node, View):
                    yield from node
                else:
                    yield node

    def _get_instance(self: Self) -> Self:
        return self

    @final
    def __str__(self) -> str:
        return "".join(self)

    def __repr__(self) -> str:
        return "<markupy.View>"

    # Allow starlette Response.render to directly render this element without
    # explicitly casting to str:
    # https://github.com/encode/starlette/blob/5ed55c441126687106109a3f5e051176f88cd3e6/starlette/responses.py#L44-L49
    def encode(self, encoding: str = "utf-8", errors: str = "strict") -> bytes:
        return str(self).encode(encoding, errors)

    __html__ = __str__
