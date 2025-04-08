from abc import abstractmethod
from collections.abc import Iterator
from typing import final

from ..exception import MarkupyError
from .fragment import Fragment
from .view import View


class Component(Fragment):
    __slots__ = ()

    def __init__(self) -> None:
        # Implementation here is useless but allows for a nice
        # argument-less super().__init__() autocomplete in user's IDE
        super().__init__()

    @abstractmethod
    def render(self) -> View: ...

    @final
    def render_content(self) -> View:
        if self._children:
            if len(self._children) == 1 and isinstance(self._children[0], View):
                # Only 1 view child: return it
                return self._children[0]
            else:
                # One non-view child or multiple children: wrap in a fragment
                return Fragment()[self._children]
        else:
            # No children: return empty view
            return View()

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
