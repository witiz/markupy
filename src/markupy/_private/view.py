from collections.abc import Callable, Iterable, Iterator, Sequence
from typing import TypeAlias, final

from markupsafe import Markup, escape

Node: TypeAlias = None | bool | str | int | Iterable["Node"] | Callable[[], "Node"]


def validate_node(node: Node) -> bool:
    if node is None or isinstance(node, bool):
        return False
    if isinstance(node, (int, View, Iterator)) or callable(node):
        return True
    if isinstance(node, str):
        return bool(node)
    elif isinstance(node, Sequence):
        return any(validate_node(child) for child in node)
    else:
        raise TypeError(f"{node!r} is not a valid child element")


def iter_node(node: Node) -> Iterator[str]:
    if not validate_node(node):
        return
    while not isinstance(node, View) and callable(node):
        node = node()
    if isinstance(node, View):
        yield from node
    elif isinstance(node, int):
        yield str(node)
    elif isinstance(node, str):
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
