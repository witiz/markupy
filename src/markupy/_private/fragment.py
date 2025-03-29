from collections.abc import Iterator
from copy import copy
from typing import final

from typing_extensions import Self

from ..exception import MarkupyError
from .node import Node, iter_node
from .view import View


class Fragment(View):
    __slots__ = ("_children", "_shared", "_safe")

    def __init__(self, children: Node = None, safe: bool = False) -> None:
        self._children: list[str | View] | None = Fragment._children_list(
            children, safe=safe
        )
        self._shared: bool = True
        self._safe: bool = safe

    def __iter__(self) -> Iterator[str]:
        if self._children is not None:
            for node in self._children:
                if isinstance(node, View):
                    yield from node
                else:
                    yield node

    def __copy__(self) -> Self:
        return type(self)()

    @final
    def _new_instance(self: Self) -> Self:
        # When imported, elements are loaded from a shared instance
        # Make sure we re-instantiate them on setting attributes/children
        # to avoid sharing attributes/children between multiple instances
        if self._shared:
            obj = copy(self)
            obj._shared = False
            return obj
        return self

    @staticmethod
    def _children_list(node: Node, *, safe: bool) -> list[str | View] | None:
        if node is not None:
            return [s for s in iter_node(node, safe=safe)]

    # Use subscriptable [] syntax to assign children
    def __getitem__(self, node: Node) -> Self:
        if self._children is not None:
            raise MarkupyError(f"Illegal attempt to redefine children of `{self!r}`")

        if new_children := Fragment._children_list(node, safe=self._safe):
            instance = self._new_instance()
            instance._children = new_children
            return instance

        return self
