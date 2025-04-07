from copy import copy
from typing import final

from typing_extensions import Self

from .view import View


class Fragment(View):
    _shared: bool = True

    def __init__(self, *, safe: bool = False) -> None:
        super().__init__(safe=safe)

    def __copy__(self) -> Self:
        return type(self)()

    def __repr__(self) -> str:
        return "<markupy.Fragment>"

    def __call__(self) -> Self:
        return self

    @final
    def _get_instance(self: Self) -> Self:
        # When imported, elements are loaded from a shared instance
        # Make sure we re-instantiate them on setting attributes/children
        # to avoid sharing attributes/children between multiple instances
        if self._shared:
            obj = copy(self)
            obj._shared = False
            return obj
        return self

    # Avoid having Django "call" a markupy fragment (or element) that is injected into a template.
    # Setting do_not_call_in_templates will prevent Django from doing an extra call:
    # https://docs.djangoproject.com/en/5.0/ref/templates/api/#variables-and-lookups
    do_not_call_in_templates = True
