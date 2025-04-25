from markupy import Attribute, attribute_handlers
from markupy import elements as el


def test_class_replace() -> None:
    def handler(old: Attribute | None, new: Attribute) -> Attribute | None:
        if new.name == "class":
            return new
        return None

    # register_attribute_handler(handler)
    attribute_handlers.register(handler)
    element = el.Input(".foo", class_="bar")
    attribute_handlers.unregister(handler)

    assert element == """<input class="bar">"""
