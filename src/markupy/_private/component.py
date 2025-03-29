from abc import ABCMeta, abstractmethod
from collections.abc import Iterator
from typing import final

from .fragment import Fragment
from .node import Node
from .view import View


class Component(View, metaclass=ABCMeta):
    @abstractmethod
    def render(self) -> Node: ...

    @final
    def __iter__(self) -> Iterator[str]:
        yield from Fragment(self.render())
