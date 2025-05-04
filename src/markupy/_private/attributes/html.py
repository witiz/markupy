from collections.abc import Iterable, Mapping
from typing import Callable, Literal

from . import Attribute, AttributeValue
from .store import python_to_html_key

# Special functions


def getattr(name: str) -> Callable[[AttributeValue], Attribute]:
    return lambda value: Attribute(python_to_html_key(name), value)


# Html Attributes


def accept(*value: str) -> Attribute:
    return Attribute("accept", ",".join(value))


def accept_charset(value: str) -> Attribute:
    return Attribute("accept-charset", value)


def accesskey(value: str) -> Attribute:
    return Attribute("accesskey", value)


def action(value: str) -> Attribute:
    return Attribute("action", value)


def align(value: str) -> Attribute:
    return Attribute("align", value)


def allow(value: str) -> Attribute:
    return Attribute("allow", value)


def alt(value: str) -> Attribute:
    return Attribute("alt", value)


def as_(value: str) -> Attribute:
    return Attribute("as", value)


def async_(value: bool = True) -> Attribute:
    return Attribute("async", value)


def autocapitalize(
    value: Literal["off", "none", "on", "sentences", "words", "characters"],
) -> Attribute:
    return Attribute("autocapitalize", value)


def autocomplete(value: Literal["on", "off"]) -> Attribute:
    return Attribute("autocomplete", value)


def autofocus(value: bool = True) -> Attribute:
    return Attribute("autofocus", value)


def autoplay(value: bool = True) -> Attribute:
    return Attribute("autoplay", value)


def background(value: str) -> Attribute:
    return Attribute("background", value)


def bgcolor(value: str) -> Attribute:
    return Attribute("bgcolor", value)


def border(value: str) -> Attribute:
    return Attribute("border", value)


def capture(value: str) -> Attribute:
    return Attribute("capture", value)


def charset(value: str) -> Attribute:
    return Attribute("charset", value)


def checked(value: bool = True) -> Attribute:
    return Attribute("checked", value)


def cite(value: str) -> Attribute:
    return Attribute("cite", value)


def class_(value: str | Iterable[str] | Mapping[str, bool]) -> Attribute:
    classes: list[str]
    if isinstance(value, str):
        classes = [value]
    elif isinstance(value, Mapping):
        classes = [k for k, v in value.items() if v]  # type: ignore[unused-ignore]
    else:
        classes = list(value)
    return Attribute("class", " ".join(classes))


def color(value: str) -> Attribute:
    return Attribute("color", value)


def cols(value: int) -> Attribute:
    return Attribute("cols", value)


def colspan(value: int) -> Attribute:
    return Attribute("colspan", value)


def content(value: str) -> Attribute:
    return Attribute("content", value)


def contenteditable(value: Literal["true", "false", ""]) -> Attribute:
    return Attribute("contenteditable", value)


def controls(value: bool = True) -> Attribute:
    return Attribute("controls", value)


def coords(value: str) -> Attribute:
    return Attribute("coords", value)


def crossorigin(value: Literal["anonymous", "use-credentials"]) -> Attribute:
    return Attribute("crossorigin", value)


def csp(value: str) -> Attribute:
    return Attribute("csp", value)


def data(value: str) -> Attribute:
    return Attribute("data", value)


def datetime(value: str) -> Attribute:
    return Attribute("datetime", value)


def decoding(value: Literal["sync", "async", "auto"]) -> Attribute:
    return Attribute("decoding", value)


def default(value: bool = True) -> Attribute:
    return Attribute("default", value)


def defer(value: bool = True) -> Attribute:
    return Attribute("defer", value)


def dir(value: Literal["ltr", "rtl", "auto"]) -> Attribute:
    return Attribute("dir", value)


def dirname(value: str) -> Attribute:
    return Attribute("dirname", value)


def disabled(value: bool = True) -> Attribute:
    return Attribute("disabled", value)


def download(value: str) -> Attribute:
    return Attribute("download", value)


def draggable(value: Literal["true", "false", "auto"]) -> Attribute:
    return Attribute("draggable", value)


def enctype(
    value: Literal[
        "application/x-www-form-urlencoded", "multipart/form-data", "text/plain"
    ],
) -> Attribute:
    return Attribute("enctype", value)


def enterkeyhint(
    value: Literal["enter", "done", "go", "next", "previous", "search", "send"],
) -> Attribute:
    return Attribute("enterkeyhint", value)


def elementtiming(value: str) -> Attribute:
    return Attribute("elementtiming", value)


def for_(value: str) -> Attribute:
    return Attribute("for", value)


def form(value: str) -> Attribute:
    return Attribute("form", value)


def formaction(value: str) -> Attribute:
    return Attribute("formaction", value)


def formenctype(
    value: Literal[
        "application/x-www-form-urlencoded", "multipart/form-data", "text/plain"
    ],
) -> Attribute:
    return Attribute("formenctype", value)


def formmethod(value: Literal["get", "post"]) -> Attribute:
    return Attribute("formmethod", value)


def formnovalidate(value: bool = True) -> Attribute:
    return Attribute("formnovalidate", value)


def formtarget(value: str) -> Attribute:
    return Attribute("formtarget", value)


def headers(value: str) -> Attribute:
    return Attribute("headers", value)


def height(value: int | str) -> Attribute:
    return Attribute("height", value)


def hidden(value: bool | Literal["until-found"] = True) -> Attribute:
    return Attribute("hidden", value)


def high(value: str) -> Attribute:
    return Attribute("high", value)


def href(value: str) -> Attribute:
    return Attribute("href", value)


def hreflang(value: str) -> Attribute:
    return Attribute("hreflang", value)


def http_equiv(
    value: Literal[
        "content-security-policy", "content-type", "default-style", "refresh"
    ],
) -> Attribute:
    return Attribute("http-equiv", value)


def id(value: str) -> Attribute:
    return Attribute("id", value)


def inputmode(
    value: Literal[
        "none", "text", "decimal", "numeric", "tel", "search", "email", "url"
    ],
) -> Attribute:
    return Attribute("inputmode", value)


def integrity(value: str) -> Attribute:
    return Attribute("integrity", value)


def ismap(value: bool = True) -> Attribute:
    return Attribute("ismap", value)


def itemprop(value: str) -> Attribute:
    return Attribute("itemprop", value)


def kind(
    value: Literal["subtitles", "captions", "descriptions", "chapters", "metadata"],
) -> Attribute:
    return Attribute("kind", value)


def label(value: str) -> Attribute:
    return Attribute("label", value)


def lang(value: str) -> Attribute:
    return Attribute("lang", value)


def loading(value: Literal["eager", "lazy"]) -> Attribute:
    return Attribute("loading", value)


def list_(value: str) -> Attribute:
    return Attribute("list", value)


def loop(value: bool = True) -> Attribute:
    return Attribute("loop", value)


def low(value: str) -> Attribute:
    return Attribute("low", value)


def max(value: int | float | str) -> Attribute:
    return Attribute("max", value)


def maxlength(value: int) -> Attribute:
    return Attribute("maxlength", value)


def media(value: str) -> Attribute:
    return Attribute("media", value)


def method(value: Literal["get", "post"]) -> Attribute:
    return Attribute("method", value)


def min(value: int | float | str) -> Attribute:
    return Attribute("min", value)


def minlength(value: int) -> Attribute:
    return Attribute("minlength", value)


def multiple(value: bool = True) -> Attribute:
    return Attribute("multiple", value)


def muted(value: bool = True) -> Attribute:
    return Attribute("muted", value)


def name(value: str) -> Attribute:
    return Attribute("name", value)


def novalidate(value: bool = True) -> Attribute:
    return Attribute("novalidate", value)


def onabort(value: str) -> Attribute:
    return Attribute("onabort", value)


def onautocomplete(value: str) -> Attribute:
    return Attribute("onautocomplete", value)


def onautocompleteerror(value: str) -> Attribute:
    return Attribute("onautocompleteerror", value)


def onblur(value: str) -> Attribute:
    return Attribute("onblur", value)


def oncancel(value: str) -> Attribute:
    return Attribute("oncancel", value)


def oncanplay(value: str) -> Attribute:
    return Attribute("oncanplay", value)


def oncanplaythrough(value: str) -> Attribute:
    return Attribute("oncanplaythrough", value)


def onchange(value: str) -> Attribute:
    return Attribute("onchange", value)


def onclick(value: str) -> Attribute:
    return Attribute("onclick", value)


def onclose(value: str) -> Attribute:
    return Attribute("onclose", value)


def oncontextmenu(value: str) -> Attribute:
    return Attribute("oncontextmenu", value)


def oncuechange(value: str) -> Attribute:
    return Attribute("oncuechange", value)


def ondblclick(value: str) -> Attribute:
    return Attribute("ondblclick", value)


def ondrag(value: str) -> Attribute:
    return Attribute("ondrag", value)


def ondragend(value: str) -> Attribute:
    return Attribute("ondragend", value)


def ondragenter(value: str) -> Attribute:
    return Attribute("ondragenter", value)


def ondragexit(value: str) -> Attribute:
    return Attribute("ondragexit", value)


def ondragleave(value: str) -> Attribute:
    return Attribute("ondragleave", value)


def ondragover(value: str) -> Attribute:
    return Attribute("ondragover", value)


def ondragstart(value: str) -> Attribute:
    return Attribute("ondragstart", value)


def ondrop(value: str) -> Attribute:
    return Attribute("ondrop", value)


def ondurationchange(value: str) -> Attribute:
    return Attribute("ondurationchange", value)


def onemptied(value: str) -> Attribute:
    return Attribute("onemptied", value)


def onended(value: str) -> Attribute:
    return Attribute("onended", value)


def onerror(value: str) -> Attribute:
    return Attribute("onerror", value)


def onfocus(value: str) -> Attribute:
    return Attribute("onfocus", value)


def onformdata(value: str) -> Attribute:
    return Attribute("onformdata", value)


def oninput(value: str) -> Attribute:
    return Attribute("oninput", value)


def oninvalid(value: str) -> Attribute:
    return Attribute("oninvalid", value)


def onkeydown(value: str) -> Attribute:
    return Attribute("onkeydown", value)


def onkeypress(value: str) -> Attribute:
    return Attribute("onkeypress", value)


def onkeyup(value: str) -> Attribute:
    return Attribute("onkeyup", value)


def onload(value: str) -> Attribute:
    return Attribute("onload", value)


def onloadeddata(value: str) -> Attribute:
    return Attribute("onloadeddata", value)


def onloadedmetadata(value: str) -> Attribute:
    return Attribute("onloadedmetadata", value)


def onloadstart(value: str) -> Attribute:
    return Attribute("onloadstart", value)


def onmousedown(value: str) -> Attribute:
    return Attribute("onmousedown", value)


def onmouseenter(value: str) -> Attribute:
    return Attribute("onmouseenter", value)


def onmouseleave(value: str) -> Attribute:
    return Attribute("onmouseleave", value)


def onmousemove(value: str) -> Attribute:
    return Attribute("onmousemove", value)


def onmouseout(value: str) -> Attribute:
    return Attribute("onmouseout", value)


def onmouseover(value: str) -> Attribute:
    return Attribute("onmouseover", value)


def onmouseup(value: str) -> Attribute:
    return Attribute("onmouseup", value)


def onpause(value: str) -> Attribute:
    return Attribute("onpause", value)


def onplay(value: str) -> Attribute:
    return Attribute("onplay", value)


def onplaying(value: str) -> Attribute:
    return Attribute("onplaying", value)


def onprogress(value: str) -> Attribute:
    return Attribute("onprogress", value)


def onratechange(value: str) -> Attribute:
    return Attribute("onratechange", value)


def onreset(value: str) -> Attribute:
    return Attribute("onreset", value)


def onresize(value: str) -> Attribute:
    return Attribute("onresize", value)


def onscroll(value: str) -> Attribute:
    return Attribute("onscroll", value)


def onsecuritypolicyviolation(value: str) -> Attribute:
    return Attribute("onsecuritypolicyviolation", value)


def onseeked(value: str) -> Attribute:
    return Attribute("onseeked", value)


def onseeking(value: str) -> Attribute:
    return Attribute("onseeking", value)


def onselect(value: str) -> Attribute:
    return Attribute("onselect", value)


def onslotchange(value: str) -> Attribute:
    return Attribute("onslotchange", value)


def onstalled(value: str) -> Attribute:
    return Attribute("onstalled", value)


def onsubmit(value: str) -> Attribute:
    return Attribute("onsubmit", value)


def onsuspend(value: str) -> Attribute:
    return Attribute("onsuspend", value)


def ontimeupdate(value: str) -> Attribute:
    return Attribute("ontimeupdate", value)


def ontoggle(value: str) -> Attribute:
    return Attribute("ontoggle", value)


def onvolumechange(value: str) -> Attribute:
    return Attribute("onvolumechange", value)


def onwaiting(value: str) -> Attribute:
    return Attribute("onwaiting", value)


def onwheel(value: str) -> Attribute:
    return Attribute("onwheel", value)


def open(value: bool = True) -> Attribute:
    return Attribute("open", value)


def optimum(value: str) -> Attribute:
    return Attribute("optimum", value)


def pattern(value: str) -> Attribute:
    return Attribute("pattern", value)


def ping(value: str) -> Attribute:
    return Attribute("ping", value)


def placeholder(value: str) -> Attribute:
    return Attribute("placeholder", value)


def playsinline(value: bool = True) -> Attribute:
    return Attribute("playsinline", value)


def popover(value: Literal["auto", "manual"]) -> Attribute:
    return Attribute("popover", value)


def poster(value: str) -> Attribute:
    return Attribute("poster", value)


def preload(value: Literal["auto", "metadata", "none"]) -> Attribute:
    return Attribute("preload", value)


def readonly(value: bool = True) -> Attribute:
    return Attribute("readonly", value)


def referrerpolicy(
    value: Literal[
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "same-origin",
        "strict-origin",
        "strict-origin-when-cross-origin",
        "unsafe-url",
    ],
) -> Attribute:
    return Attribute("referrerpolicy", value)


def rel(
    value: Literal[
        "alternate",
        "author",
        "bookmark",
        "canonical",
        "dns-prefetch",
        "external",
        "help",
        "icon",
        "license",
        "manifest",
        "modulepreload",
        "next",
        "nofollow",
        "noopener",
        "noreferrer",
        "opener",
        "pingback",
        "preconnect",
        "prefetch",
        "preload",
        "prev",
        "search",
        "stylesheet",
        "tag",
    ],
) -> Attribute:
    return Attribute("rel", value)


def required(value: bool = True) -> Attribute:
    return Attribute("required", value)


def reversed(value: bool = True) -> Attribute:
    return Attribute("reversed", value)


def role(value: str) -> Attribute:
    return Attribute("role", value)


def rows(value: int) -> Attribute:
    return Attribute("rows", value)


def rowspan(value: int) -> Attribute:
    return Attribute("rowspan", value)


def sandbox(
    *value: Literal[
        "allow-forms",
        "allow-modals",
        "allow-orientation-lock",
        "allow-pointer-lock",
        "allow-popups",
        "allow-presentation",
        "allow-same-origin",
        "allow-scripts",
        "allow-top-navigation",
        "allow-downloads",
        "allow-top-navigation-by-user-activation",
    ],
) -> Attribute:
    return Attribute("sandbox", " ".join(value))


def scope(value: Literal["col", "row", "colgroup", "rowgroup"]) -> Attribute:
    return Attribute("scope", value)


def selected(value: bool = True) -> Attribute:
    return Attribute("selected", value)


def shape(value: Literal["default", "rect", "circle", "poly"]) -> Attribute:
    return Attribute("shape", value)


def size(value: int) -> Attribute:
    return Attribute("size", value)


def sizes(*value: str) -> Attribute:
    return Attribute("sizes", ",".join(value))


def slot(value: str) -> Attribute:
    return Attribute("slot", value)


def span(value: int) -> Attribute:
    return Attribute("span", value)


def spellcheck(value: Literal["true", "false"] | bool = True) -> Attribute:
    return Attribute("spellcheck", value)


def src(value: str) -> Attribute:
    return Attribute("src", value)


def srcdoc(value: str) -> Attribute:
    return Attribute("srcdoc", value)


def srclang(value: str) -> Attribute:
    return Attribute("srclang", value)


def srcset(*value: str) -> Attribute:
    return Attribute("srcset", ",".join(value))


def start(value: str) -> Attribute:
    return Attribute("start", value)


def step(value: int | float | Literal["any"]) -> Attribute:
    return Attribute("step", value)


def style(value: str) -> Attribute:
    return Attribute("style", value)


def tabindex(value: int) -> Attribute:
    return Attribute("tabindex", value)


def target(
    value: Literal["_self", "_blank", "_parent", "_top"] | str,
) -> Attribute:
    return Attribute("target", value)


def title(value: str) -> Attribute:
    return Attribute("title", value)


def translate(value: Literal["yes", "no"]) -> Attribute:
    return Attribute("translate", value)


def type_(
    value: Literal[
        "button",
        "checkbox",
        "color",
        "date",
        "datetime-local",
        "email",
        "file",
        "hidden",
        "image",
        "month",
        "number",
        "password",
        "radio",
        "range",
        "reset",
        "search",
        "submit",
        "tel",
        "text",
        "time",
        "url",
        "week",
    ],
) -> Attribute:
    return Attribute("type", value)


def usemap(value: str) -> Attribute:
    return Attribute("usemap", value)


def value(value: str | int | float) -> Attribute:
    return Attribute("value", value)


def virtualkeyboardpolicy(
    value: Literal["auto", "manual"] = "auto",
) -> Attribute:
    return Attribute("virtualkeyboardpolicy", value)


def writingsuggestions(value: bool = True) -> Attribute:
    return Attribute("writingsuggestions", value)


def width(value: int | str) -> Attribute:
    return Attribute("width", value)


def wrap(value: Literal["hard", "soft", "off"]) -> Attribute:
    return Attribute("wrap", value)
