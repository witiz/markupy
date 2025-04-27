from copy import copy
from typing import final

from typing_extensions import Self

from .view import View


class Fragment(View):
    __slots__ = ("_shared",)

    def __init__(self, *, safe: bool = False, shared: bool = True) -> None:
        super().__init__(safe=safe)
        self._shared: bool = shared

    def __copy__(self) -> Self:
        return type(self)(shared=False)

    def __call__(self) -> Self:
        return self

    @final
    def _get_instance(self: Self) -> Self:
        # When imported, elements are loaded from a shared instance
        # Make sure we re-instantiate them on setting attributes/children
        # to avoid sharing attributes/children between multiple instances
        if self._shared:
            return copy(self)
        return self

    # Avoid having Django "call" a markupy fragment (or element) that is injected into a template.
    # Setting do_not_call_in_templates will prevent Django from doing an extra call:
    # https://docs.djangoproject.com/en/5.0/ref/templates/api/#variables-and-lookups
    do_not_call_in_templates = True
