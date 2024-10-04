from html.parser import HTMLParser
from json import dumps as json_dumps
from keyword import iskeyword
from re import sub as re_sub
from typing import Iterator

from markupsafe import escape

from markupy import tag

from .attribute import is_boolean_attribute
from .element import VoidElement

_void_elements: set[str] = {
    element.name
    for element in map(lambda x: getattr(tag, x), tag.__all__)
    if isinstance(element, VoidElement)
}


def _is_void_element(name: str) -> bool:
    return name in _void_elements


def _format_attribute_key(key: str) -> str:
    if iskeyword(key):
        return f"{key}_"
    if key.startswith("@"):
        key = f"_{key[1:]}"
    parts = key.split("-")
    key = f"{parts[0]}{''.join(map(lambda x: x.capitalize(), parts[1:]))}"
    key = key.replace(":", "__")
    key = key.replace(".", "_")
    return key


def _format_attribute_value(value: str | None) -> str:
    if value is None:
        return "True"
    return json_dumps(value)


def _format_attrs_dict(attrs: dict[str, str | None]) -> str:
    return "{" + ",".join(f'"{key}":{value}' for key, value in attrs.items()) + "}"


# Process attrs as they are received from the html parser
def _format_attrs(
    attrs: list[tuple[str, str | None]], *, use_selector: bool
) -> str | None:
    if not attrs:
        return None

    arguments: list[str] = []

    selector: str = ""
    attrs_kwargs: list[str] = list()
    attrs_dict: dict[str, str | None] = dict()

    for key, value in attrs:
        if is_boolean_attribute(key):
            value = None
        elif not value:
            continue
        elif key == "id" and use_selector and "{" not in value:
            selector = f"#{value}{selector}"
            continue
        elif key == "class" and use_selector and "{" not in value:
            selector = f"{selector}.{'.'.join(value.split())}"
            continue

        py_key = _format_attribute_key(key)
        if py_key.isidentifier():
            attrs_kwargs.append(f"{py_key}={_format_attribute_value(value)}")
        else:
            attrs_dict[key] = _format_attribute_value(value)

    if selector:
        arguments.append(f'"{selector}"')
    if attrs_kwargs:
        arguments += attrs_kwargs
    if attrs_dict:
        arguments.append(_format_attrs_dict(attrs_dict))

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
            raise ValueError("Can't push None or empty string into stack")
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
    def __init__(self, *, use_selector: bool, use_import_tag: bool) -> None:
        self.count_top_level: int = 0
        self.code_stack: Stack = Stack()
        self.unclosed_stack: Stack = Stack()
        self.imports: set[str] = set()
        self.use_import_tag: bool = use_import_tag
        self.use_selector: bool = use_selector
        super().__init__()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # print("Encountered a start tag:", tag, attrs)
        if len(self.unclosed_stack) == 0:
            self.count_top_level += 1
        if not _is_void_element(tag):
            self.unclosed_stack.push(tag)

        markupy_tag = "".join(map(lambda x: x.capitalize(), tag.split("-")))
        if self.use_import_tag:
            markupy_tag = f"tag.{markupy_tag}"

        self.imports.add(markupy_tag)
        self.code_stack.push(markupy_tag)
        if attributes_str := _format_attrs(attrs, use_selector=self.use_selector):
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
                raise ValueError(f"Unexpected closing tag `</{tag}>`")
            elif tag != "endblock" and tag != last_open_tag:
                raise ValueError(
                    f"Invalid closing tag `</{tag}>`, expected `</{last_open_tag}>`"
                )
            elif tag == "endblock" and not last_open_tag.startswith("block-"):
                raise ValueError(
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
        if self.imports:
            if self.use_import_tag:
                return "from markupy import tag\n"
            else:
                return f"from markupy.tag import {','.join(sorted(self.imports))}\n"
        return ""

    def output_code(self) -> str:
        code = "".join(self.code_stack).strip(",")
        if self.count_top_level > 1:
            return f"[{code}]"
        return code


def _template_process(html: str) -> str:
    # Replace opening `block`
    html = re_sub(
        r"{%[+-]?\s+block\s+([a-zA-Z_]+)\s+[+-]?%}",
        lambda match: f"<block-{match.group(1).lower().replace('_','-')}>",
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
    html: str, *, use_selector: bool = True, use_import_tag: bool = False
) -> str:
    parser = MarkupyParser(use_selector=use_selector, use_import_tag=use_import_tag)
    parser.feed(_template_process(html))
    parser.close()
    if tag := parser.unclosed_stack.pop():
        raise ValueError(f"Opening tag `<{tag}>` was not closed")
    if code := parser.output_code():
        return f"{parser.output_imports()}{code}"
    return ""
