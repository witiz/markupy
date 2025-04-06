from collections.abc import Iterable, Iterator
from copy import copy
from typing import Any, final

from markupsafe import escape
from typing_extensions import Self

from ..exception import MarkupyError
from .view import View


def iter_node(node: Any, *, safe: bool = False) -> Iterator[str | View]:
    if node is None or node == "" or isinstance(node, bool):
        return
    elif isinstance(node, View):
        # View is callable and Iterable, must be checked in priority
        # callable views are Element and Fragment instances
        yield node
    elif callable(node):
        # Allows to catch uncalled functions or uninstanciated classes
        raise MarkupyError(
            f"Invalid node `{node!r}`. Did you mean `{node.__name__}()` ?"
        )
    elif isinstance(node, Iterable) and not isinstance(node, str):
        for child in node:  # type: ignore[unused-ignore]
            yield from iter_node(child, safe=safe)
    elif safe:
        yield str(node)
    else:
        yield str(escape(node))


class Fragment(View):
    __slots__ = ("_children", "_shared", "_safe")

    def __init__(self, *, safe: bool = False) -> None:
        self._children: list[str | View] | None = None
        self._shared: bool = True
        self._safe: bool = safe

    def __copy__(self) -> Self:
        return type(self)()

    def __repr__(self) -> str:
        return "<markupy.Fragment>"

    # Use subscriptable [] syntax to assign children
    def __getitem__(self, node: Any) -> Self:
        if self._children is not None:
            raise MarkupyError(f"Illegal attempt to redefine children of `{self!r}`")

        try:
            children = list(iter_node(node, safe=self._safe))
        except Exception as e:
            raise MarkupyError(f"Invalid child provided for {self!r}") from e

        if children:
            instance = self._get_instance()
            instance._children = children
            return instance

        return self

    def __iter__(self) -> Iterator[str]:
        if self._children is not None:
            for node in self._children:
                if isinstance(node, View):
                    yield from node
                else:
                    yield node

    @final
    def _get_instance(self: Self) -> Self:
        # When imported, elements are loaded from a shared instance
        # Make sure we re-instantiate them on setting attributes/children
        # to avoid sharing attributes/children between multiple instances
        if self._shared:
            obj = copy(self)
            obj._shared = False
            return obj
        return self

    def __call__(self) -> Self:
        return self

    # Avoid having Django "call" a markupy fragment (or element) that is injected into a template.
    # Setting do_not_call_in_templates will prevent Django from doing an extra call:
    # https://docs.djangoproject.com/en/5.0/ref/templates/api/#variables-and-lookups
    do_not_call_in_templates = True
