from typing import Any, Sequence

from markupy import View


def pytest_assertrepr_compare(op: str, left: Any, right: Any) -> Sequence[str] | None:
    l_repr = f"`{left}`" if isinstance(left, View) else repr(left)
    r_repr = f"`{right}`" if isinstance(right, View) else repr(right)
    return [op, l_repr, r_repr]
