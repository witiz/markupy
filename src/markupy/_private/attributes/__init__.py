from .attribute import Attribute, AttributeValue
from .handlers import attribute_handlers
from .html import HtmlAttributes
from .store import AttributeStore

attributes = HtmlAttributes()

__all__ = [
    "attribute_handlers",
    "attributes",
    "Attribute",
    "AttributeValue",
    "AttributeStore",
]
