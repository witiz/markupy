from collections.abc import Iterable, Iterator
from inspect import isclass, isfunction, ismethod
from typing import Any, TypeAlias, final

from markupsafe import Markup, escape
from typing_extensions import Self

from ...exceptions import MarkupyError

ChildType: TypeAlias = "str | View"
ChildrenType: TypeAlias = tuple[ChildType, ...]


class View:
    __slots__ = ("_children", "_safe")

    def __init__(self, *, safe: bool = False) -> None:
        super().__init__()
        self._children: ChildrenType = tuple()
        self._safe: bool = safe

    @final
    def __str__(self) -> str:
        # Return needs to be Markup and not plain str
        # to be properly injected in template engines
        return Markup("".join(self))

    @final
    def __html__(self) -> str:
        return str(self)

    @final
    def __eq__(self, other: object) -> bool:
        return str(other) == str(self)

    @final
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return "<markupy.View>"

    def __iter__(self) -> Iterator[str]:
        for node in self._children:
            if isinstance(node, View):
                yield from node
            else:
                yield node

    def _iter_node(self, node: Any) -> Iterator[ChildType]:
        if node is None or isinstance(node, bool):
            return
        elif isinstance(node, View):
            # View is Iterable, must check in priority
            yield node
        elif isinstance(node, Iterable) and not isinstance(node, str):
            for child in node:  # type: ignore[unused-ignore]
                yield from self._iter_node(child)
        elif isfunction(node) or ismethod(node) or isclass(node):
            # Allows to catch uncalled functions/methods or uninstanciated classes
            raise MarkupyError(
                f"Invalid child node {node!r} provided for {self!r}; Did you mean `{node.__name__}()` ?"
            )
        else:
            try:
                if s := str(node if self._safe else escape(node)):
                    yield s
            except Exception as e:
                raise MarkupyError(
                    f"Invalid child node {node!r} provided for {self!r}"
                ) from e

    # Use subscriptable [] syntax to assign children
    def __getitem__(self, content: Any) -> Self:
        if self._children:
            raise MarkupyError(f"Illegal attempt to redefine children of {self!r}")

        if children := tuple(self._iter_node(content)):
            instance = self._get_instance()
            instance._children = children
            return instance

        return self

    def _get_instance(self: Self) -> Self:
        return self

    # Allow starlette Response.render to directly render this element without
    # explicitly casting to str:
    # https://github.com/encode/starlette/blob/5ed55c441126687106109a3f5e051176f88cd3e6/starlette/responses.py#L44-L49
    @final
    def encode(self, encoding: str = "utf-8", errors: str = "strict") -> bytes:
        return str(self).encode(encoding, errors)
