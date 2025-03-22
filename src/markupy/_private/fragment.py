from collections.abc import Iterator
from copy import copy
from typing import final

from typing_extensions import Self

from .node import Node, iter_node, validate_node
from .view import View


class Fragment(View):
    __slots__ = ("_children", "_shared", "_safe")

    def __init__(self) -> None:
        self._children: Node = None
        self._shared: bool = True
        self._safe: bool = False

    def __iter__(self) -> Iterator[str]:
        yield from iter_node(self._children)

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

    # Use subscriptable [] syntax to assign children
    def __getitem__(self, children: Node) -> Self:
        if self._children is not None:
            raise Exception(f"Illegal attempt to redefine children for element {self}")
        elif validate_node(children):
            instance = self._new_instance()
            instance._children = children
            return instance

        return self
