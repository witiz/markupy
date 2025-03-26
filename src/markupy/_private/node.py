from collections.abc import Callable, Generator, Iterable, Iterator
from typing import TypeAlias

from markupsafe import Markup, escape

from .exception import MarkupyError
from .view import View

Node: TypeAlias = None | bool | str | int | Iterable["Node"] | Callable[[], "Node"]

ValidNode = str | int | View | Callable | Generator  # type: ignore[type-arg]
InvalidNode = bytes | bytearray | memoryview


def _is_empty_node(node: Node) -> bool:
    return node is None or node is True or node is False or node == ""


def validate_node(node: Node) -> bool:
    if _is_empty_node(node):
        return False
    elif isinstance(node, ValidNode):
        return True
    elif isinstance(node, Iterable) and not isinstance(node, InvalidNode):
        # Must return True if any child is valid
        # Must return False if all child not valid
        # Must loop over all items to raise exception any invalid child
        for child in node:
            if validate_node(child):
                return True
        return False
    else:
        raise MarkupyError(f"{node!r} is not a valid child element")


def iter_node(node: Node, *, safe: bool = False) -> Iterator[str]:
    if _is_empty_node(node):
        return
    while not isinstance(node, View) and callable(node):
        node = node()

    if isinstance(node, str):
        if isinstance(node, Markup):
            yield node
        elif safe:
            yield Markup(node)
        else:
            yield str(escape(node))
    elif isinstance(node, Iterable):
        if isinstance(node, View):
            yield from node
        else:
            for child in node:
                yield from iter_node(child, safe=safe)
    elif isinstance(node, int):
        yield str(node)
    else:
        raise MarkupyError(f"{node!r} is not a valid child element")
