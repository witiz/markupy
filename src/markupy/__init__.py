from ._private.attribute import Attribute, register_attribute_handler
from ._private.component import Component
from ._private.fragment import Fragment as _Fragment
from ._private.html import to_markupy as html2markupy
from ._private.view import View

Fragment = _Fragment()

__all__ = [
    "Attribute",
    "Component",
    "Fragment",
    "View",
    "html2markupy",
    "register_attribute_handler",
]
__version__ = "2.1.0"
