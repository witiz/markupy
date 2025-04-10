from collections.abc import Iterator
from typing import final

from markupsafe import Markup


class View:
    __slots__ = ()

    def __init__(self) -> None:
        super().__init__()

    def __iter__(self) -> Iterator[str]:
        yield from ()

    @final
    def __str__(self) -> str:
        # Return needs to be Markup and not plain str
        # to be properly injected in template engines
        return Markup("".join(self))

    def __repr__(self) -> str:
        return "<markupy.View>"

    # Allow starlette Response.render to directly render this element without
    # explicitly casting to str:
    # https://github.com/encode/starlette/blob/5ed55c441126687106109a3f5e051176f88cd3e6/starlette/responses.py#L44-L49
    def encode(self, encoding: str = "utf-8", errors: str = "strict") -> bytes:
        return str(self).encode(encoding, errors)

    __html__ = __str__
