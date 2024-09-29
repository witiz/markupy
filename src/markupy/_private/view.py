from abc import ABC, abstractmethod
from collections.abc import Callable, Generator, Iterable, Iterator
from typing import TypeAlias, final

from markupsafe import Markup, escape

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


class View(Iterable[str]):
    @final
    def __str__(self) -> str:
        return Markup("".join(self))

    # Allow starlette Response.render to directly render this element without
    # explicitly casting to str:
    # https://github.com/encode/starlette/blob/5ed55c441126687106109a3f5e051176f88cd3e6/starlette/responses.py#L44-L49
    def encode(self, encoding: str = "utf-8", errors: str = "strict") -> bytes:
        return str(self).encode(encoding, errors)

    # Avoid having Django "call" a markupy element that is injected into a
    # template. Setting do_not_call_in_templates will prevent Django from doing
    # an extra call:
    # https://docs.djangoproject.com/en/5.0/ref/templates/api/#variables-and-lookups
    do_not_call_in_templates = True


class Component(ABC, View):
    @abstractmethod
    def render(self) -> Node: ...

    @final
    def __iter__(self) -> Iterator[str]:
        yield from iter_node(self.render())
