from abc import ABCMeta, abstractmethod
from collections.abc import Iterator
from typing import final

from .node import Node, iter_node
from .view import View


class Component(View, metaclass=ABCMeta):
    @abstractmethod
    def render(self) -> Node: ...

    @final
    def __iter__(self) -> Iterator[str]:
        yield from iter_node(self.render())
