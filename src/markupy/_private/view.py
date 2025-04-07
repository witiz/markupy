from collections.abc import Iterable, Iterator
from typing import final


class View(Iterable[str]):
    def __iter__(self) -> Iterator[str]:
        yield ""

    @final
    def __str__(self) -> str:
        return "".join(self)

    def __repr__(self) -> str:
        return "<markupy.View>"

    # Allow starlette Response.render to directly render this element without
    # explicitly casting to str:
    # https://github.com/encode/starlette/blob/5ed55c441126687106109a3f5e051176f88cd3e6/starlette/responses.py#L44-L49
    def encode(self, encoding: str = "utf-8", errors: str = "strict") -> bytes:
        return str(self).encode(encoding, errors)

    __html__ = __str__
