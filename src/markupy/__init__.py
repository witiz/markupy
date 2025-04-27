from ._private.attributes import Attribute, attribute_handlers
from ._private.attributes import HtmlAttributes as _HtmlAttributes
from ._private.html_to_markupy import html_to_markupy
from ._private.views import Component, View
from ._private.views import Fragment as _Fragment

Fragment = _Fragment()
attributes = _HtmlAttributes()

__all__ = [
    "Attribute",
    "Component",
    "Fragment",
    "View",
    "attribute_handlers",
    "attributes",
    "html_to_markupy",
]
__version__ = "2.2.0"
