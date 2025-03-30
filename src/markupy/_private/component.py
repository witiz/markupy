from abc import ABCMeta, abstractmethod
from collections.abc import Iterator
from typing import final

from ..exception import MarkupyError
from .view import View


class Component(View, metaclass=ABCMeta):
    @abstractmethod
    def render(self) -> View: ...

    @final
    def __iter__(self) -> Iterator[str]:
        node = self.render()
        if isinstance(node, View):  # type: ignore[unused-ignore]
            yield from node
        else:
            raise MarkupyError(
                f"{type(self).__name__}.render() must return an instance of markupy.View (can be Element, Fragment or Component)"
            )
