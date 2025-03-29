from collections.abc import Iterable, Iterator
from typing import TypeAlias

from markupsafe import escape

from ..exception import MarkupyError
from .view import View

Node: TypeAlias = None | bool | str | int | Iterable["Node"]


def iter_node(node: Node, *, safe: bool = False) -> Iterator[str | View]:
    # bool is int
    if isinstance(node, bool):
        return
    # str is Iterable
    elif isinstance(node, str | int):
        if node == "":
            return
        elif safe:
            yield str(node)
        else:
            yield str(escape(node))
    # View is Iterable
    elif isinstance(node, View):
        yield node
    elif isinstance(node, Iterable):
        for child in node:
            yield from iter_node(child, safe=safe)
    elif node is None:
        return
    else:
        raise MarkupyError(f"{node!r} is not a valid child element")
