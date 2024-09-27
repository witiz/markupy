from functools import lru_cache
from re import match as re_fullmatch
from re import sub as re_sub

from ._private.element import CommentElement, Element, HtmlElement, VoidElement

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


@lru_cache(maxsize=300)
def _get_element(name: str) -> Element:
    if not re_fullmatch(r"^(?:[A-Z][a-z]*)+$", name):
        raise AttributeError(
            f"{name} is not a valid element name. markupy tags must be in CapitalizedCase"
        )

    #  Uppercase chars are word boundaries for tag names
    words = filter(None, re_sub(r"([A-Z])", r" \1", name).split())
    html_name = "-".join(words).lower()
    return Element(html_name)


def __getattr__(name: str) -> Element:
    return _get_element(name)


_ = CommentElement("_")

# https://developer.mozilla.org/en-US/docs/Glossary/Doctype
Html = HtmlElement("html")

# https://developer.mozilla.org/en-US/docs/Glossary/Void_element
Area = VoidElement("area")
Base = VoidElement("base")
Br = VoidElement("br")
Col = VoidElement("col")
Embed = VoidElement("embed")
Hr = VoidElement("hr")
Img = VoidElement("img")
Input = VoidElement("input")
Link = VoidElement("link")
Meta = VoidElement("meta")
Param = VoidElement("param")
Source = VoidElement("source")
Track = VoidElement("track")
Wbr = VoidElement("wbr")

# Non-deprecated HTML elements, extracted from
# https://developer.mozilla.org/en-US/docs/Web/HTML/Element
# Located via the inspector with:
# Array.from($0.querySelectorAll('li')).filter(x=>!x.querySelector('.icon-deprecated')).map(x => x.querySelector('code').textContent) # noqa: E501
A = Element("a")
Abbr = Element("abbr")
Abc = Element("abc")
Address = Element("address")
Article = Element("article")
Aside = Element("aside")
Audio = Element("audio")
B = Element("b")
Bdi = Element("bdi")
Bdo = Element("bdo")
Blockquote = Element("blockquote")
Body = Element("body")
Button = Element("button")
Canvas = Element("canvas")
Caption = Element("caption")
Cite = Element("cite")
Code = Element("code")
Colgroup = Element("colgroup")
Data = Element("data")
Datalist = Element("datalist")
Dd = Element("dd")
Del = Element("del")
Details = Element("details")
Dfn = Element("dfn")
Dialog = Element("dialog")
Div = Element("div")
Dl = Element("dl")
Dt = Element("dt")
Em = Element("em")
Fieldset = Element("fieldset")
Figcaption = Element("figcaption")
Figure = Element("figure")
Footer = Element("footer")
Form = Element("form")
H1 = Element("h1")
H2 = Element("h2")
H3 = Element("h3")
H4 = Element("h4")
H5 = Element("h5")
H6 = Element("h6")
Head = Element("head")
Header = Element("header")
Hgroup = Element("hgroup")
I = Element("i")  # noqa: E741
Iframe = Element("iframe")
Ins = Element("ins")
Kbd = Element("kbd")
Label = Element("label")
Legend = Element("legend")
Li = Element("li")
Main = Element("main")
Map = Element("map")
Mark = Element("mark")
Menu = Element("menu")
Meter = Element("meter")
Nav = Element("nav")
Noscript = Element("noscript")
Object = Element("object")
Ol = Element("ol")
Optgroup = Element("optgroup")
Option = Element("option")
Output = Element("output")
P = Element("p")
Picture = Element("picture")
Portal = Element("portal")
Pre = Element("pre")
Progress = Element("progress")
Q = Element("q")
Rp = Element("rp")
Rt = Element("rt")
Ruby = Element("ruby")
S = Element("s")
Samp = Element("samp")
Script = Element("script")
Search = Element("search")
Section = Element("section")
Select = Element("select")
Slot = Element("slot")
Small = Element("small")
Span = Element("span")
Strong = Element("strong")
Style = Element("style")
Sub = Element("sub")
Summary = Element("summary")
Sup = Element("sup")
Table = Element("table")
Tbody = Element("tbody")
Td = Element("td")
Template = Element("template")
Textarea = Element("textarea")
Tfoot = Element("tfoot")
Th = Element("th")
Thead = Element("thead")
Time = Element("time")
Title = Element("title")
Tr = Element("tr")
U = Element("u")
Ul = Element("ul")
Var = Element("var")
