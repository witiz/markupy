from .element import Element


def __getattr__(name: str) -> Element:
    return Element.shared_instance(name)
