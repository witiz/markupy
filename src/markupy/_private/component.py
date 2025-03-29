from abc import ABCMeta, abstractmethod
from collections.abc import Iterator
from typing import Any, final

from .fragment import Fragment
from .view import View


class Component(View, metaclass=ABCMeta):
    @abstractmethod
    def render(self) -> Any: ...

    @final
    def __iter__(self) -> Iterator[str]:
        yield from Fragment(self.render())
