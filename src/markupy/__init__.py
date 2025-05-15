from ._private.attributes import Attribute, attribute_handlers
from ._private.html_to_markupy import html_to_markupy
from ._private.views import Component, View
from ._private.views import Fragment as _Fragment

__all__ = [
    "Attribute",
    "Component",
    "Fragment",
    "View",
    "attribute_handlers",
    "html_to_markupy",
]
__version__ = "2.4.0"

Fragment = _Fragment()
