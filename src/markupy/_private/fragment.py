from collections.abc import Iterable, Iterator
from inspect import isclass, isfunction, ismethod
from typing import Any, TypeAlias

from markupsafe import escape
from typing_extensions import Self

from ..exception import MarkupyError
from .view import View

ChildType: TypeAlias = str | View
ChildrenType: TypeAlias = tuple[ChildType, ...]


class Fragment(View):
    __slots__ = ("_children", "_safe")

    def __init__(self, *, safe: bool = False) -> None:
        super().__init__()
        self._children: ChildrenType = tuple()
        self._safe: bool = safe

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

        if children := tuple(c for c in self._iter_node(content)):
            instance = self._get_instance()
            instance._children = children
            return instance

        return self

    def __iter__(self) -> Iterator[str]:
        for node in self._children:
            if isinstance(node, View):
                yield from node
            else:
                yield node

    def _get_instance(self: Self) -> Self:
        return self

    def __repr__(self) -> str:
        return "<markupy.Fragment>"
