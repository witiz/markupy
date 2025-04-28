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


_ = _views.CommentElement("_")

# Script and Style contents do not need to be wrapped inside Markup()
Script = _views.SafeElement("script")
Style = _views.SafeElement("style")

# https://developer.mozilla.org/en-US/docs/Glossary/Doctype
Html = _views.HtmlElement("html")

# https://developer.mozilla.org/en-US/docs/Glossary/Void_views.Element
Area = _views.VoidElement("area")
Base = _views.VoidElement("base")
Br = _views.VoidElement("br")
Col = _views.VoidElement("col")
Embed = _views.VoidElement("embed")
Hr = _views.VoidElement("hr")
Img = _views.VoidElement("img")
Input = _views.VoidElement("input")
Link = _views.VoidElement("link")
Meta = _views.VoidElement("meta")
Param = _views.VoidElement("param")
Source = _views.VoidElement("source")
Track = _views.VoidElement("track")
Wbr = _views.VoidElement("wbr")

# Non-deprecated HTML _views.Elements, extracted from
# https://developer.mozilla.org/en-US/docs/Web/HTML/Element
# Located via the inspector with:
# Array.from($0.querySelectorAll('li')).filter(x=>!x.querySelector('.icon-deprecated')).map(x => x.querySelector('code').textContent) # noqa: E501
A = _views.Element("a")
Abbr = _views.Element("abbr")
Abc = _views.Element("abc")
Address = _views.Element("address")
Article = _views.Element("article")
Aside = _views.Element("aside")
Audio = _views.Element("audio")
B = _views.Element("b")
Bdi = _views.Element("bdi")
Bdo = _views.Element("bdo")
Blockquote = _views.Element("blockquote")
Body = _views.Element("body")
Button = _views.Element("button")
Canvas = _views.Element("canvas")
Caption = _views.Element("caption")
Cite = _views.Element("cite")
Code = _views.Element("code")
Colgroup = _views.Element("colgroup")
Data = _views.Element("data")
Datalist = _views.Element("datalist")
Dd = _views.Element("dd")
Del = _views.Element("del")
Details = _views.Element("details")
Dfn = _views.Element("dfn")
Dialog = _views.Element("dialog")
Div = _views.Element("div")
Dl = _views.Element("dl")
Dt = _views.Element("dt")
Em = _views.Element("em")
Fieldset = _views.Element("fieldset")
Figcaption = _views.Element("figcaption")
Figure = _views.Element("figure")
Footer = _views.Element("footer")
Form = _views.Element("form")
H1 = _views.Element("h1")
H2 = _views.Element("h2")
H3 = _views.Element("h3")
H4 = _views.Element("h4")
H5 = _views.Element("h5")
H6 = _views.Element("h6")
Head = _views.Element("head")
Header = _views.Element("header")
Hgroup = _views.Element("hgroup")
I = _views.Element("i")  # noqa: E741
Iframe = _views.Element("iframe")
Ins = _views.Element("ins")
Kbd = _views.Element("kbd")
Label = _views.Element("label")
Legend = _views.Element("legend")
Li = _views.Element("li")
Main = _views.Element("main")
Map = _views.Element("map")
Mark = _views.Element("mark")
Menu = _views.Element("menu")
Meter = _views.Element("meter")
Nav = _views.Element("nav")
Noscript = _views.Element("noscript")
Object = _views.Element("object")
Ol = _views.Element("ol")
Optgroup = _views.Element("optgroup")
Option = _views.Element("option")
Output = _views.Element("output")
P = _views.Element("p")
Picture = _views.Element("picture")
Portal = _views.Element("portal")
Pre = _views.Element("pre")
Progress = _views.Element("progress")
Q = _views.Element("q")
Rp = _views.Element("rp")
Rt = _views.Element("rt")
Ruby = _views.Element("ruby")
S = _views.Element("s")
Samp = _views.Element("samp")
Search = _views.Element("search")
Section = _views.Element("section")
Select = _views.Element("select")
Slot = _views.Element("slot")
Small = _views.Element("small")
Span = _views.Element("span")
Strong = _views.Element("strong")
Sub = _views.Element("sub")
Summary = _views.Element("summary")
Sup = _views.Element("sup")
Table = _views.Element("table")
Tbody = _views.Element("tbody")
Td = _views.Element("td")
Template = _views.Element("template")
Textarea = _views.Element("textarea")
Tfoot = _views.Element("tfoot")
Th = _views.Element("th")
Thead = _views.Element("thead")
Time = _views.Element("time")
Title = _views.Element("title")
Tr = _views.Element("tr")
U = _views.Element("u")
Ul = _views.Element("ul")
Var = _views.Element("var")
