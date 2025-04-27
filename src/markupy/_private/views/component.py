from abc import abstractmethod
from collections.abc import Iterator
from typing import Any, final

from typing_extensions import Self

from markupy.exceptions import MarkupyError

from .view import View


class Component(View):
    __slots__ = ()

    def __init__(self) -> None:
        # Implementation here is useless but allows for a nice
        # argument-less super().__init__() autocomplete in user's IDE
        super().__init__()

    def __post_init__(self) -> None:
        # Allows for simple dataclass Component definition
        super().__init__()

    @final
    def __getitem__(self, content: Any) -> Self:
        if not hasattr(self, "_children"):
            raise MarkupyError(
                "Subclasses of <markupy.Component> must call `super().__init__()` if they override the default initializer."
            )

        return super().__getitem__(content)

    @abstractmethod
    def render(self) -> View: ...

    @final
    def render_content(self) -> View:
        # Use getattr here to avoid error in case super()__init__ hasn't been called
        if children := getattr(self, "_children", None):
            if len(children) == 1 and isinstance(children[0], View):
                # Only 1 view child: return it
                return children[0]
            else:
                # One non-view child or multiple children: wrap in a fragment
                # (do not use the [] syntax to avoid re-processing/re-escaping)
                view = View()
                view._children = children
                return view

        else:
            # No children or super().__init__() hasn't been called and we are
            # missing the _children attribute: return empty view
            return View()

    @final
    def __iter__(self) -> Iterator[str]:
        node = self.render()
        if isinstance(node, View):  # type: ignore[unused-ignore]
            yield from node
        else:
            raise MarkupyError(
                f"`{type(self).__name__}.render()` must return an instance of <markupy.View> or one of its subclasses (Element, Fragment, Component)"
            )

    @final
    def __repr__(self) -> str:
        return f"<markupy.Component.{type(self).__name__}>"
