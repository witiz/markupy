from collections.abc import Callable, Generator, Iterable, Iterator
from typing import TypeAlias, final

from markupsafe import Markup, escape

Node: TypeAlias = None | bool | str | int | Iterable["Node"] | Callable[[], "Node"]


def validate_node(node: Node) -> bool:
    if node is None or node is True or node is False:
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
    if node is None or node is True or node is False:
        return
    while not isinstance(node, View) and callable(node):
        node = node()
    if isinstance(node, View):
        yield from node
    elif isinstance(node, int):
        yield str(node)
    elif isinstance(node, str):
        if node:
            yield str(escape(node))
    elif isinstance(node, Iterable):
        for child in node:
            yield from iter_node(child)
    else:
        raise TypeError(f"{node!r} is not a valid child element")


def render_node(*node: Node) -> Markup:
    return Markup("".join(iter_node(node)))


class View(Iterable[str]):
    def render(self) -> Node:
        return None

    def __iter__(self) -> Iterator[str]:
        yield from iter_node(self.render())

    @final
    def __str__(self) -> str:
        return Markup("".join(self))
