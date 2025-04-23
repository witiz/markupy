from ._private.attribute import Attribute
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
]
__version__ = "2.0.0"
