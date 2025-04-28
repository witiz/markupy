from .attribute import Attribute, AttributeValue
from .html import HtmlAttributes
from .store import AttributeStore, attribute_handlers

attributes = HtmlAttributes()

__all__ = [
    "attribute_handlers",
    "attributes",
    "Attribute",
    "AttributeValue",
    "AttributeStore",
]
