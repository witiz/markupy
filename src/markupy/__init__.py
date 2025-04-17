from ._private.component import Component
from ._private.html import to_markupy as html2markupy
from ._private.shared import Shared
from ._private.view import View

Fragment = Shared()

__all__ = ["Component", "Fragment", "View", "html2markupy"]
__version__ = "1.4.0"
