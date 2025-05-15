from collections.abc import Mapping
from html.parser import HTMLParser
from json import dumps as json_dumps
from keyword import iskeyword
from re import sub as re_sub
from typing import Iterator

from markupsafe import escape

from ...exceptions import MarkupyError
from ..views.element import SPECIAL_ELEMENTS, VoidElement

VOID_ELEMENTS: set[str] = {
    name for name, cls in SPECIAL_ELEMENTS.items() if cls is VoidElement
}


def _is_void_element(name: str) -> bool:
    return name in VOID_ELEMENTS


# https://html.spec.whatwg.org/multipage/indices.html#attributes-3
BOOLEAN_ATTRIBUTES: set[str] = {
    "allowfullscreen",
    "async",
    "autofocus",
    "autoplay",
    "checked",
    "controls",
    "default",
    "defer",
    "disabled",
    "formnovalidate",
    "inert",
    "ismap",
    "itemscope",
    "loop",
    "multiple",
    "muted",
    "nomodule",
    "novalidate",
    "open",
    "playsinline",
    "readonly",
    "required",
    "reversed",
    "selected",
}


def _is_boolean_attribute(name: str) -> bool:
    return name in BOOLEAN_ATTRIBUTES


def _format_attribute_key(key: str) -> str | None:
    pykey = key.replace("-", "_")
    if pykey.isidentifier():
        if iskeyword(pykey):
            # Escape python reserved keywords
            return f"{pykey}_"
        return pykey
    return None


def _format_attribute_value(value: str | None) -> str:
    if value is None:
        return "True"
    return json_dumps(value)


def _format_attrs_dict(attrs: Mapping[str, str | None]) -> str:
    return "{" + ",".join(f'"{key}":{value}' for key, value in attrs.items()) + "}"


# Process attrs as they are received from the html parser
def _format_attrs(
    attrs: list[tuple[str, str | None]], *, use_selector: bool, use_dict: bool
) -> str | None:
    if not attrs:
        return None

    arguments: list[str] = []

    selector: str = ""
    attrs_kwargs: list[str] = list()
    attrs_dict: dict[str, str | None] = dict()

    for key, value in attrs:
        if _is_boolean_attribute(key):
            value = None
        elif not value:
            continue
        elif key == "id" and use_selector and "{" not in value:
            selector = f"#{value}{selector}"
            continue
        elif key == "class" and use_selector and "{" not in value:
            selector = f"{selector}.{'.'.join(value.split())}"
            continue

        if use_dict:
            attrs_dict[key] = _format_attribute_value(value)
        else:
            if py_key := _format_attribute_key(key):
                attrs_kwargs.append(f"{py_key}={_format_attribute_value(value)}")
            else:
                attrs_dict[key] = _format_attribute_value(value)

    if selector:
        arguments.append(_format_attribute_value(selector))
    if attrs_dict:
        arguments.append(_format_attrs_dict(attrs_dict))
    if attrs_kwargs:
        arguments += attrs_kwargs

    if len(arguments) > 0:
        return f"({','.join(arguments)})"

    return None


class Stack:
    def __init__(self) -> None:
        self._list: list[str] = []

    def __len__(self) -> int:
        return len(self._list)

    def push(self, item: str) -> None:
        if not item:
            raise MarkupyError("Can't push None or empty string into stack")
        self._list.append(item)

    def peek(self) -> str | None:
        if len(self) > 0:
            return self._list[-1]
        return None

    def pop(self) -> str | None:
        if len(self) > 0:
            return self._list.pop()
        return None

    def __iter__(self) -> Iterator[str]:
        yield from self._list


class MarkupyParser(HTMLParser):
    def __init__(
        self, *, use_selector: bool, use_dict: bool, use_import_el: bool
    ) -> None:
        self.count_top_level: int = 0
        self.code_stack: Stack = Stack()
        self.unclosed_stack: Stack = Stack()
        self.imports: set[str] = set()
        self.use_import_el: bool = use_import_el
        self.use_dict: bool = use_dict
        self.use_selector: bool = use_selector
        super().__init__()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # print("Encountered a start tag:", tag, attrs)
        if len(self.unclosed_stack) == 0:
            self.count_top_level += 1
        if not _is_void_element(tag):
            self.unclosed_stack.push(tag)

        markupy_tag = "".join(map(lambda x: x.capitalize(), tag.split("-")))
        if self.use_import_el:
            markupy_tag = f"el.{markupy_tag}"

        self.imports.add(markupy_tag)
        self.code_stack.push(markupy_tag)
        if attributes_str := _format_attrs(
            attrs, use_selector=self.use_selector, use_dict=self.use_dict
        ):
            self.code_stack.push(attributes_str)
        if _is_void_element(tag):
            self.code_stack.push(",")
        else:
            self.code_stack.push("[")

    def handle_endtag(self, tag: str) -> None:
        # print("Encountered an end tag :", tag)
        if not _is_void_element(tag):
            last_open_tag = self.unclosed_stack.pop()
            if last_open_tag is None:
                raise MarkupyError(f"Unexpected closing tag `</{tag}>`")
            elif tag != "endblock" and tag != last_open_tag:
                raise MarkupyError(
                    f"Invalid closing tag `</{tag}>`, expected `</{last_open_tag}>`"
                )
            elif tag == "endblock" and not last_open_tag.startswith("block-"):
                raise MarkupyError(
                    f"Invalid template `endblock`, expected `</{last_open_tag}>`"
                )

        if self.code_stack.peek() == ",":
            self.code_stack.pop()
        if self.code_stack.peek() == "[":
            self.code_stack.pop()
        elif not _is_void_element(tag):
            self.code_stack.push("]")
        self.code_stack.push(",")

    def handle_data(self, data: str) -> None:
        # print("Encountered some data  :", data)
        for line in data.splitlines():
            # Strip newlines, leading/traing spaces and redundant spaces
            line = " ".join(line.split())
            if not line:
                continue
            if len(self.unclosed_stack) == 0:
                self.count_top_level += 1
            self.code_stack.push(json_dumps(line))
            self.code_stack.push(",")

    def output_imports(self) -> str:
        str_markupy_imports: str = ""
        str_markupy_tag_imports: str = ""
        markupy_imports: set[str] = set()
        if self.count_top_level > 1:
            markupy_imports.add("Fragment")
        if self.imports:
            if self.use_import_el:
                markupy_imports.add("elements as el")
                # return "from markupy import tag\n"
            else:
                str_markupy_tag_imports = (
                    f"from markupy.elements import {','.join(sorted(self.imports))}\n"
                )
        if markupy_imports:
            str_markupy_imports = (
                f"from markupy import {','.join(sorted(markupy_imports))}\n"
            )
        return str_markupy_imports + str_markupy_tag_imports

    def output_code(self) -> str:
        code = "".join(self.code_stack).strip(",")
        if self.count_top_level > 1:
            return f"Fragment[{code}]"
        return code


def _template_process(html: str) -> str:
    # Replace opening `block`
    html = re_sub(
        r"{%[+-]?\s+block\s+([a-zA-Z_]+)\s+[+-]?%}",
        lambda match: f"<block-{match.group(1).lower().replace('_', '-')}>",
        html,
    )
    # Replace closing `block`
    html = re_sub(
        r"{%[+-]?\s+endblock(?:\s+[a-zA-Z_]+)?\s+[+-]?%}",
        # we can use whatever closing tag name we want here as it'll end up being replace with a closing bracket
        "</endblock>",
        html,
    )
    # Escape template contents
    html = re_sub(
        r"{{.*?}}|{%.*?%}|{#.*?#}",
        lambda match: escape(match.group(0)),
        html,
    )
    return html


def to_markupy(
    html: str,
    *,
    use_selector: bool = True,
    use_dict: bool = False,
    use_import_el: bool = False,
) -> str:
    parser = MarkupyParser(
        use_selector=use_selector, use_dict=use_dict, use_import_el=use_import_el
    )
    parser.feed(_template_process(html))
    parser.close()
    if tag := parser.unclosed_stack.pop():
        raise MarkupyError(f"Opening tag `<{tag}>` was not closed")
    if code := parser.output_code():
        return f"{parser.output_imports()}{code}"
    return ""
