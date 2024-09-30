from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import TYPE_CHECKING, final

from .view import View

if TYPE_CHECKING:
    from .node import Node


class Component(ABC, View):
    @abstractmethod
    def render(self) -> "Node": ...

    @final
    def __iter__(self) -> Iterator[str]:
        from .node import iter_node

        yield from iter_node(self.render())
