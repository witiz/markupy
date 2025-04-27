from ._private.views import CommentElement as _CommentElement
from ._private.views import Element as _Element
from ._private.views import HtmlElement as _HtmlElement
from ._private.views import SafeElement as _SafeElement
from ._private.views import VoidElement as _VoidElement
from ._private.views import get_element as _get_element

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


def __getattr__(name: str) -> _Element:
    return _get_element(name)


_ = _CommentElement("_")

# Script and Style contents do not need to be wrapped inside Markup()
Script = _SafeElement("script")
Style = _SafeElement("style")

# https://developer.mozilla.org/en-US/docs/Glossary/Doctype
Html = _HtmlElement("html")

# https://developer.mozilla.org/en-US/docs/Glossary/Void_element
Area = _VoidElement("area")
Base = _VoidElement("base")
Br = _VoidElement("br")
Col = _VoidElement("col")
Embed = _VoidElement("embed")
Hr = _VoidElement("hr")
Img = _VoidElement("img")
Input = _VoidElement("input")
Link = _VoidElement("link")
Meta = _VoidElement("meta")
Param = _VoidElement("param")
Source = _VoidElement("source")
Track = _VoidElement("track")
Wbr = _VoidElement("wbr")

# Non-deprecated HTML _Elements, extracted from
# https://developer.mozilla.org/en-US/docs/Web/HTML/Element
# Located via the inspector with:
# Array.from($0.querySelectorAll('li')).filter(x=>!x.querySelector('.icon-deprecated')).map(x => x.querySelector('code').textContent) # noqa: E501
A = _Element("a")
Abbr = _Element("abbr")
Abc = _Element("abc")
Address = _Element("address")
Article = _Element("article")
Aside = _Element("aside")
Audio = _Element("audio")
B = _Element("b")
Bdi = _Element("bdi")
Bdo = _Element("bdo")
Blockquote = _Element("blockquote")
Body = _Element("body")
Button = _Element("button")
Canvas = _Element("canvas")
Caption = _Element("caption")
Cite = _Element("cite")
Code = _Element("code")
Colgroup = _Element("colgroup")
Data = _Element("data")
Datalist = _Element("datalist")
Dd = _Element("dd")
Del = _Element("del")
Details = _Element("details")
Dfn = _Element("dfn")
Dialog = _Element("dialog")
Div = _Element("div")
Dl = _Element("dl")
Dt = _Element("dt")
Em = _Element("em")
Fieldset = _Element("fieldset")
Figcaption = _Element("figcaption")
Figure = _Element("figure")
Footer = _Element("footer")
Form = _Element("form")
H1 = _Element("h1")
H2 = _Element("h2")
H3 = _Element("h3")
H4 = _Element("h4")
H5 = _Element("h5")
H6 = _Element("h6")
Head = _Element("head")
Header = _Element("header")
Hgroup = _Element("hgroup")
I = _Element("i")  # noqa: E741
Iframe = _Element("iframe")
Ins = _Element("ins")
Kbd = _Element("kbd")
Label = _Element("label")
Legend = _Element("legend")
Li = _Element("li")
Main = _Element("main")
Map = _Element("map")
Mark = _Element("mark")
Menu = _Element("menu")
Meter = _Element("meter")
Nav = _Element("nav")
Noscript = _Element("noscript")
Object = _Element("object")
Ol = _Element("ol")
Optgroup = _Element("optgroup")
Option = _Element("option")
Output = _Element("output")
P = _Element("p")
Picture = _Element("picture")
Portal = _Element("portal")
Pre = _Element("pre")
Progress = _Element("progress")
Q = _Element("q")
Rp = _Element("rp")
Rt = _Element("rt")
Ruby = _Element("ruby")
S = _Element("s")
Samp = _Element("samp")
Search = _Element("search")
Section = _Element("section")
Select = _Element("select")
Slot = _Element("slot")
Small = _Element("small")
Span = _Element("span")
Strong = _Element("strong")
Sub = _Element("sub")
Summary = _Element("summary")
Sup = _Element("sup")
Table = _Element("table")
Tbody = _Element("tbody")
Td = _Element("td")
Template = _Element("template")
Textarea = _Element("textarea")
Tfoot = _Element("tfoot")
Th = _Element("th")
Thead = _Element("thead")
Time = _Element("time")
Title = _Element("title")
Tr = _Element("tr")
U = _Element("u")
Ul = _Element("ul")
Var = _Element("var")
