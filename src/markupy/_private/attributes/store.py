from collections.abc import Mapping
from functools import lru_cache

from markupy.exceptions import MarkupyError

from .attribute import Attribute, AttributeValue
from .handlers import attribute_handlers


@attribute_handlers.register
def default_attribute_handler(
    old: Attribute | None, new: Attribute
) -> Attribute | None:
    if old is None or old.value is None or old.value == new.value:
        # Prefer returning None instead of new here for multiple reasons:
        # - better performance
        # - do not rely on presence of handler to persist attributes
        # Attribute redefinition is allowed if values are equal
        # this is useful when bundling attrs into "traits" tuples
        # that may overlap with each other
        return None
    elif new.value is None:
        new.value = old.value
        return None
    elif new.name == "class":
        # For class, attribute redefinition is allowed:
        # new values get appended to old values and then deduplicated
        merged = f"{old.value} {new.value}"
        new.value = " ".join(dict.fromkeys(merged.split()))
        return None

    raise MarkupyError(f"Invalid attempt to redefine attribute `{new.name}`")


@lru_cache(maxsize=1000)
def python_to_html_key(key: str) -> str:
    if not key.isidentifier():
        # Might happen when using the **{} syntax
        raise MarkupyError(f"Attribute `{key}` has invalid name")
    if key == "_":
        # Preserve single underscore for hyperscript compatibility
        return key
    # Trailing underscore "_" is meaningless and is used to escape protected
    # keywords that might be used as attr keys such as class_ and for_
    # Underscores become dashes
    return key.removesuffix("_").replace("_", "-")


class AttributeStore(dict[str, Attribute]):
    __slots__ = ()

    def __setitem__(self, key: str, new: Attribute) -> None:
        old = self[key] if key in self else None
        for handler in attribute_handlers:
            if attribute := handler(old, new):
                if attribute is new:
                    # stop the handler chain
                    new = attribute
                    break
                else:
                    # restart a handler chain (beware of infinite loops!)
                    return self.add(attribute)

        super().__setitem__(key, new)

    def __str__(self) -> str:
        return " ".join(filter(None, map(str, self.values())))

    def add_selector(self, selector: str) -> None:
        if selector := selector.replace(".", " ").strip():
            if "#" in selector[1:]:
                raise MarkupyError(
                    "Id must be defined only once and must be in first position of selector"
                )
            if selector.startswith("#"):
                rawid, *classes = selector.split()
                if id := rawid[1:]:
                    self.add(Attribute("id", id))
            else:
                classes = selector.split()

            if classes:
                self.add(Attribute("class", " ".join(classes)))

    def add_dict(
        self,
        dct: Mapping[str, AttributeValue],
        *,
        rewrite_keys: bool = False,
    ) -> None:
        for key, value in dct.items():
            name = python_to_html_key(key) if rewrite_keys else key
            self.add(Attribute(name, value))

    def add(self, new: Attribute) -> None:
        self[new.name] = new
