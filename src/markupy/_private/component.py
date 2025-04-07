from abc import abstractmethod
from collections.abc import Iterator
from typing import final

from ..exception import MarkupyError
from .view import View


class Component(View):
    __slots__ = ()

    def __init__(self) -> None:
        # Implementation here is useless but allows for a nice
        # argument-less super().__init__() autocomplete in user's IDE
        super().__init__()

    @abstractmethod
    def render(self) -> View: ...

    @final
    def content(self) -> list[str | View] | None:
        return self._children

    @final
    def __iter__(self) -> Iterator[str]:
        node = self.render()
        if isinstance(node, View):  # type: ignore[unused-ignore]
            yield from node
        else:
            raise MarkupyError(
                f"{type(self).__name__}.render() must return an instance of markupy.View (can be Element, Fragment or Component)"
            )

    @final
    def __repr__(self) -> str:
        return f"<markupy.Component.{type(self).__name__}>"
