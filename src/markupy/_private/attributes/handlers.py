from collections.abc import Iterator
from typing import Callable

from markupy.exceptions import MarkupyError

from .attribute import Attribute

# We prefer this signature over (name:str, old_value:AttributeValue, new_value:AttributeValue)
# for several reasons:
# - avoid exposing AttributeValue type that is too low level
# - allows to differentiate between an attribute that has never been instanciated vs
#   an attribute that has already been instanciated with a None value
AttributeHandler = Callable[[Attribute | None, Attribute], Attribute | None]


class AttributeHandlerRegistry(dict[AttributeHandler, None]):
    def register(self, handler: AttributeHandler) -> AttributeHandler:
        """Registers the handler and returns it unchanged (so usable as a decorator)."""
        if handler in self:
            raise MarkupyError(f"Handler {handler.__name__} is already registered.")
        self[handler] = None
        return handler  # Important for decorator usage

    def unregister(self, handler: AttributeHandler) -> None:
        self.pop(handler, None)

    def __iter__(self) -> Iterator[AttributeHandler]:
        yield from reversed(self.keys())


attribute_handlers = AttributeHandlerRegistry()
