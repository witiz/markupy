from abc import ABCMeta, abstractmethod
from collections.abc import Iterator
from typing import final

from .view import View


class Component(View, metaclass=ABCMeta):
    @abstractmethod
    def render(self) -> View: ...

    @final
    def __iter__(self) -> Iterator[str]:
        yield from self.render()
