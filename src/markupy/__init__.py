from ._private.attribute import Attribute, attribute_handlers
from ._private.component import Component
from ._private.fragment import Fragment as _Fragment
from ._private.html import to_markupy as html2markupy
from ._private.html_attributes import HtmlAttributes as _HtmlAttributes
from ._private.view import View

Fragment = _Fragment()
attributes = _HtmlAttributes()

__all__ = [
    "Attribute",
    "Component",
    "Fragment",
    "View",
    "attribute_handlers",
    "attributes",
    "html2markupy",
]
__version__ = "2.2.0"
