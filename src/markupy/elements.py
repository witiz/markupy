from ._private import views as _views

__all__ = [
    "_",
    "Html",
    "Area",
    "Base",
    "Br",
    "Col",
    "Embed",
    "Hr",
    "Img",
    "Input",
    "Link",
    "Meta",
    "Param",
    "Source",
    "Track",
    "Wbr",
    "A",
    "Abbr",
    "Abc",
    "Address",
    "Article",
    "Aside",
    "Audio",
    "B",
    "Bdi",
    "Bdo",
    "Blockquote",
    "Body",
    "Button",
    "Canvas",
    "Caption",
    "Cite",
    "Code",
    "Colgroup",
    "Data",
    "Datalist",
    "Dd",
    "Del",
    "Details",
    "Dfn",
    "Dialog",
    "Div",
    "Dl",
    "Dt",
    "Em",
    "Fieldset",
    "Figcaption",
    "Figure",
    "Footer",
    "Form",
    "H1",
    "H2",
    "H3",
    "H4",
    "H5",
    "H6",
    "Head",
    "Header",
    "Hgroup",
    "I",
    "Iframe",
    "Ins",
    "Kbd",
    "Label",
    "Legend",
    "Li",
    "Main",
    "Map",
    "Mark",
    "Menu",
    "Meter",
    "Nav",
    "Noscript",
    "Object",
    "Ol",
    "Optgroup",
    "Option",
    "Output",
    "P",
    "Picture",
    "Portal",
    "Pre",
    "Progress",
    "Q",
    "Rp",
    "Rt",
    "Ruby",
    "S",
    "Samp",
    "Script",
    "Search",
    "Section",
    "Select",
    "Slot",
    "Small",
    "Span",
    "Strong",
    "Style",
    "Sub",
    "Summary",
    "Sup",
    "Table",
    "Tbody",
    "Td",
    "Template",
    "Textarea",
    "Tfoot",
    "Th",
    "Thead",
    "Time",
    "Title",
    "Tr",
    "U",
    "Ul",
    "Var",
]


def __getattr__(name: str) -> _views.Element:
    return _views.get_element(name)


_: _views.Element
A: _views.Element
Abbr: _views.Element
Abc: _views.Element
Address: _views.Element
Area: _views.Element
Article: _views.Element
Aside: _views.Element
Audio: _views.Element
B: _views.Element
Base: _views.Element
Bdi: _views.Element
Bdo: _views.Element
Blockquote: _views.Element
Body: _views.Element
Br: _views.Element
Button: _views.Element
Canvas: _views.Element
Caption: _views.Element
Cite: _views.Element
Code: _views.Element
Col: _views.Element
Colgroup: _views.Element
Data: _views.Element
Datalist: _views.Element
Dd: _views.Element
Del: _views.Element
Details: _views.Element
Dfn: _views.Element
Dialog: _views.Element
Div: _views.Element
Dl: _views.Element
Dt: _views.Element
Em: _views.Element
Embed: _views.Element
Fieldset: _views.Element
Figcaption: _views.Element
Figure: _views.Element
Footer: _views.Element
Form: _views.Element
H1: _views.Element
H2: _views.Element
H3: _views.Element
H4: _views.Element
H5: _views.Element
H6: _views.Element
Head: _views.Element
Header: _views.Element
Hgroup: _views.Element
Hr: _views.Element
Html: _views.Element
I: _views.Element  # noqa: E741
Iframe: _views.Element
Img: _views.Element
Input: _views.Element
Ins: _views.Element
Kbd: _views.Element
Label: _views.Element
Legend: _views.Element
Li: _views.Element
Link: _views.Element
Main: _views.Element
Map: _views.Element
Mark: _views.Element
Menu: _views.Element
Meta: _views.Element
Meter: _views.Element
Nav: _views.Element
Noscript: _views.Element
Object: _views.Element
Ol: _views.Element
Optgroup: _views.Element
Option: _views.Element
Output: _views.Element
P: _views.Element
Param: _views.Element
Picture: _views.Element
Portal: _views.Element
Pre: _views.Element
Progress: _views.Element
Q: _views.Element
Rp: _views.Element
Rt: _views.Element
Ruby: _views.Element
S: _views.Element
Samp: _views.Element
Script: _views.Element
Search: _views.Element
Section: _views.Element
Select: _views.Element
Slot: _views.Element
Small: _views.Element
Source: _views.Element
Span: _views.Element
Strong: _views.Element
Style: _views.Element
Sub: _views.Element
Summary: _views.Element
Sup: _views.Element
Table: _views.Element
Tbody: _views.Element
Td: _views.Element
Template: _views.Element
Textarea: _views.Element
Tfoot: _views.Element
Th: _views.Element
Thead: _views.Element
Time: _views.Element
Title: _views.Element
Tr: _views.Element
Track: _views.Element
U: _views.Element
Ul: _views.Element
Var: _views.Element
Wbr: _views.Element
