from collections.abc import Callable, Generator, Iterable, Iterator
from typing import TypeAlias

from markupsafe import Markup, escape

from .view import View

Node: TypeAlias = None | bool | str | int | Iterable["Node"] | Callable[[], "Node"]


def _is_empty_node(node: Node) -> bool:
    return node is None or node is True or node is False or node == ""


def validate_node(node: Node) -> bool:
    if _is_empty_node(node):
        return False

    valid_nodes = str | int | View | Callable | Generator  # type: ignore[type-arg]
    invalid_nodes = bytes | bytearray | memoryview
    if isinstance(node, valid_nodes):
        return True
    elif isinstance(node, Iterable) and not isinstance(node, invalid_nodes):
        # Must return True if any child is valid
        # Must return False if all child not valid
        # Must loop over all items to raise exception any invalid child
        result = False
        for child in node:
            if validate_node(child):
                result = True
        return result
    else:
        raise TypeError(f"{node!r} is not a valid child element")


def iter_node(node: Node) -> Iterator[str]:
    if _is_empty_node(node):
        return
    while not isinstance(node, View) and callable(node):
        node = node()

    if isinstance(node, str):
        if isinstance(node, Markup):
            yield node
        else:
            yield str(escape(node))
    elif isinstance(node, Iterable):
        if isinstance(node, View):
            yield from node
        else:
            for child in node:
                yield from iter_node(child)
    elif isinstance(node, int):
        yield str(node)
    else:
        raise TypeError(f"{node!r} is not a valid child element")


def render_node(*node: Node) -> Markup:
    return Markup("".join(iter_node(node)))
