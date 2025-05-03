from collections.abc import Iterable, Mapping
from typing import Callable, Literal

from . import Attribute, AttributeValue
from .store import python_to_html_key


class HtmlAttributes:
    def __getattr__(self, name: str) -> Callable[[AttributeValue], Attribute]:
        return lambda value: Attribute(python_to_html_key(name), value)

    def __call__(self, name: str, value: AttributeValue) -> Attribute:
        return Attribute(name, value)

    def accept(self, *value: str) -> Attribute:
        return Attribute("accept", ",".join(value))

    def accept_charset(self, value: str) -> Attribute:
        return Attribute("accept-charset", value)

    def accesskey(self, value: str) -> Attribute:
        return Attribute("accesskey", value)

    def action(self, value: str) -> Attribute:
        return Attribute("action", value)

    def align(self, value: str) -> Attribute:
        return Attribute("align", value)

    def allow(self, value: str) -> Attribute:
        return Attribute("allow", value)

    def alt(self, value: str) -> Attribute:
        return Attribute("alt", value)

    def as_(self, value: str) -> Attribute:
        return Attribute("as", value)

    def async_(self, value: bool = True) -> Attribute:
        return Attribute("async", value)

    def autocapitalize(
        self,
        value: Literal["off", "none", "on", "sentences", "words", "characters"],
    ) -> Attribute:
        return Attribute("autocapitalize", value)

    def autocomplete(self, value: Literal["on", "off"]) -> Attribute:
        return Attribute("autocomplete", value)

    def autofocus(self, value: bool = True) -> Attribute:
        return Attribute("autofocus", value)

    def autoplay(self, value: bool = True) -> Attribute:
        return Attribute("autoplay", value)

    def background(self, value: str) -> Attribute:
        return Attribute("background", value)

    def bgcolor(self, value: str) -> Attribute:
        return Attribute("bgcolor", value)

    def border(self, value: str) -> Attribute:
        return Attribute("border", value)

    def capture(self, value: str) -> Attribute:
        return Attribute("capture", value)

    def charset(self, value: str) -> Attribute:
        return Attribute("charset", value)

    def checked(self, value: bool = True) -> Attribute:
        return Attribute("checked", value)

    def cite(self, value: str) -> Attribute:
        return Attribute("cite", value)

    def class_(self, value: str | Iterable[str] | Mapping[str, bool]) -> Attribute:
        classes: list[str]
        if isinstance(value, str):
            classes = [value]
        elif isinstance(value, Mapping):
            classes = [k for k, v in value.items() if v]  # type: ignore[unused-ignore]
        else:
            classes = list(value)
        return Attribute("class", " ".join(classes))

    def color(self, value: str) -> Attribute:
        return Attribute("color", value)

    def cols(self, value: int) -> Attribute:
        return Attribute("cols", value)

    def colspan(self, value: int) -> Attribute:
        return Attribute("colspan", value)

    def content(self, value: str) -> Attribute:
        return Attribute("content", value)

    def contenteditable(self, value: Literal["true", "false", ""]) -> Attribute:
        return Attribute("contenteditable", value)

    def controls(self, value: bool = True) -> Attribute:
        return Attribute("controls", value)

    def coords(self, value: str) -> Attribute:
        return Attribute("coords", value)

    def crossorigin(self, value: Literal["anonymous", "use-credentials"]) -> Attribute:
        return Attribute("crossorigin", value)

    def csp(self, value: str) -> Attribute:
        return Attribute("csp", value)

    def data(self, value: str) -> Attribute:
        return Attribute("data", value)

    def datetime(self, value: str) -> Attribute:
        return Attribute("datetime", value)

    def decoding(self, value: Literal["sync", "async", "auto"]) -> Attribute:
        return Attribute("decoding", value)

    def default(self, value: bool = True) -> Attribute:
        return Attribute("default", value)

    def defer(self, value: bool = True) -> Attribute:
        return Attribute("defer", value)

    def dir(self, value: Literal["ltr", "rtl", "auto"]) -> Attribute:
        return Attribute("dir", value)

    def dirname(self, value: str) -> Attribute:
        return Attribute("dirname", value)

    def disabled(self, value: bool = True) -> Attribute:
        return Attribute("disabled", value)

    def download(self, value: str) -> Attribute:
        return Attribute("download", value)

    def draggable(self, value: Literal["true", "false", "auto"]) -> Attribute:
        return Attribute("draggable", value)

    def enctype(
        self,
        value: Literal[
            "application/x-www-form-urlencoded", "multipart/form-data", "text/plain"
        ],
    ) -> Attribute:
        return Attribute("enctype", value)

    def enterkeyhint(
        self,
        value: Literal["enter", "done", "go", "next", "previous", "search", "send"],
    ) -> Attribute:
        return Attribute("enterkeyhint", value)

    def elementtiming(self, value: str) -> Attribute:
        return Attribute("elementtiming", value)

    def for_(self, value: str) -> Attribute:
        return Attribute("for", value)

    def form(self, value: str) -> Attribute:
        return Attribute("form", value)

    def formaction(self, value: str) -> Attribute:
        return Attribute("formaction", value)

    def formenctype(
        self,
        value: Literal[
            "application/x-www-form-urlencoded", "multipart/form-data", "text/plain"
        ],
    ) -> Attribute:
        return Attribute("formenctype", value)

    def formmethod(self, value: Literal["get", "post"]) -> Attribute:
        return Attribute("formmethod", value)

    def formnovalidate(self, value: bool = True) -> Attribute:
        return Attribute("formnovalidate", value)

    def formtarget(self, value: str) -> Attribute:
        return Attribute("formtarget", value)

    def headers(self, value: str) -> Attribute:
        return Attribute("headers", value)

    def height(self, value: int | str) -> Attribute:
        return Attribute("height", value)

    def hidden(self, value: bool | Literal["until-found"] = True) -> Attribute:
        return Attribute("hidden", value)

    def high(self, value: str) -> Attribute:
        return Attribute("high", value)

    def href(self, value: str) -> Attribute:
        return Attribute("href", value)

    def hreflang(self, value: str) -> Attribute:
        return Attribute("hreflang", value)

    def http_equiv(
        self,
        value: Literal[
            "content-security-policy", "content-type", "default-style", "refresh"
        ],
    ) -> Attribute:
        return Attribute("http-equiv", value)

    def id(self, value: str) -> Attribute:
        return Attribute("id", value)

    def inputmode(
        self,
        value: Literal[
            "none", "text", "decimal", "numeric", "tel", "search", "email", "url"
        ],
    ) -> Attribute:
        return Attribute("inputmode", value)

    def integrity(self, value: str) -> Attribute:
        return Attribute("integrity", value)

    def ismap(self, value: bool = True) -> Attribute:
        return Attribute("ismap", value)

    def itemprop(self, value: str) -> Attribute:
        return Attribute("itemprop", value)

    def kind(
        self,
        value: Literal["subtitles", "captions", "descriptions", "chapters", "metadata"],
    ) -> Attribute:
        return Attribute("kind", value)

    def label(self, value: str) -> Attribute:
        return Attribute("label", value)

    def lang(self, value: str) -> Attribute:
        return Attribute("lang", value)

    def loading(self, value: Literal["eager", "lazy"]) -> Attribute:
        return Attribute("loading", value)

    def list(self, value: str) -> Attribute:
        return Attribute("list", value)

    def loop(self, value: bool = True) -> Attribute:
        return Attribute("loop", value)

    def low(self, value: str) -> Attribute:
        return Attribute("low", value)

    def max(self, value: int | float | str) -> Attribute:
        return Attribute("max", value)

    def maxlength(self, value: int) -> Attribute:
        return Attribute("maxlength", value)

    def media(self, value: str) -> Attribute:
        return Attribute("media", value)

    def method(self, value: Literal["get", "post"]) -> Attribute:
        return Attribute("method", value)

    def min(self, value: int | float | str) -> Attribute:
        return Attribute("min", value)

    def minlength(self, value: int) -> Attribute:
        return Attribute("minlength", value)

    def multiple(self, value: bool = True) -> Attribute:
        return Attribute("multiple", value)

    def muted(self, value: bool = True) -> Attribute:
        return Attribute("muted", value)

    def name(self, value: str) -> Attribute:
        return Attribute("name", value)

    def novalidate(self, value: bool = True) -> Attribute:
        return Attribute("novalidate", value)

    def onabort(self, value: str) -> Attribute:
        return Attribute("onabort", value)

    def onautocomplete(self, value: str) -> Attribute:
        return Attribute("onautocomplete", value)

    def onautocompleteerror(self, value: str) -> Attribute:
        return Attribute("onautocompleteerror", value)

    def onblur(self, value: str) -> Attribute:
        return Attribute("onblur", value)

    def oncancel(self, value: str) -> Attribute:
        return Attribute("oncancel", value)

    def oncanplay(self, value: str) -> Attribute:
        return Attribute("oncanplay", value)

    def oncanplaythrough(self, value: str) -> Attribute:
        return Attribute("oncanplaythrough", value)

    def onchange(self, value: str) -> Attribute:
        return Attribute("onchange", value)

    def onclick(self, value: str) -> Attribute:
        return Attribute("onclick", value)

    def onclose(self, value: str) -> Attribute:
        return Attribute("onclose", value)

    def oncontextmenu(self, value: str) -> Attribute:
        return Attribute("oncontextmenu", value)

    def oncuechange(self, value: str) -> Attribute:
        return Attribute("oncuechange", value)

    def ondblclick(self, value: str) -> Attribute:
        return Attribute("ondblclick", value)

    def ondrag(self, value: str) -> Attribute:
        return Attribute("ondrag", value)

    def ondragend(self, value: str) -> Attribute:
        return Attribute("ondragend", value)

    def ondragenter(self, value: str) -> Attribute:
        return Attribute("ondragenter", value)

    def ondragexit(self, value: str) -> Attribute:
        return Attribute("ondragexit", value)

    def ondragleave(self, value: str) -> Attribute:
        return Attribute("ondragleave", value)

    def ondragover(self, value: str) -> Attribute:
        return Attribute("ondragover", value)

    def ondragstart(self, value: str) -> Attribute:
        return Attribute("ondragstart", value)

    def ondrop(self, value: str) -> Attribute:
        return Attribute("ondrop", value)

    def ondurationchange(self, value: str) -> Attribute:
        return Attribute("ondurationchange", value)

    def onemptied(self, value: str) -> Attribute:
        return Attribute("onemptied", value)

    def onended(self, value: str) -> Attribute:
        return Attribute("onended", value)

    def onerror(self, value: str) -> Attribute:
        return Attribute("onerror", value)

    def onfocus(self, value: str) -> Attribute:
        return Attribute("onfocus", value)

    def onformdata(self, value: str) -> Attribute:
        return Attribute("onformdata", value)

    def oninput(self, value: str) -> Attribute:
        return Attribute("oninput", value)

    def oninvalid(self, value: str) -> Attribute:
        return Attribute("oninvalid", value)

    def onkeydown(self, value: str) -> Attribute:
        return Attribute("onkeydown", value)

    def onkeypress(self, value: str) -> Attribute:
        return Attribute("onkeypress", value)

    def onkeyup(self, value: str) -> Attribute:
        return Attribute("onkeyup", value)

    def onload(self, value: str) -> Attribute:
        return Attribute("onload", value)

    def onloadeddata(self, value: str) -> Attribute:
        return Attribute("onloadeddata", value)

    def onloadedmetadata(self, value: str) -> Attribute:
        return Attribute("onloadedmetadata", value)

    def onloadstart(self, value: str) -> Attribute:
        return Attribute("onloadstart", value)

    def onmousedown(self, value: str) -> Attribute:
        return Attribute("onmousedown", value)

    def onmouseenter(self, value: str) -> Attribute:
        return Attribute("onmouseenter", value)

    def onmouseleave(self, value: str) -> Attribute:
        return Attribute("onmouseleave", value)

    def onmousemove(self, value: str) -> Attribute:
        return Attribute("onmousemove", value)

    def onmouseout(self, value: str) -> Attribute:
        return Attribute("onmouseout", value)

    def onmouseover(self, value: str) -> Attribute:
        return Attribute("onmouseover", value)

    def onmouseup(self, value: str) -> Attribute:
        return Attribute("onmouseup", value)

    def onpause(self, value: str) -> Attribute:
        return Attribute("onpause", value)

    def onplay(self, value: str) -> Attribute:
        return Attribute("onplay", value)

    def onplaying(self, value: str) -> Attribute:
        return Attribute("onplaying", value)

    def onprogress(self, value: str) -> Attribute:
        return Attribute("onprogress", value)

    def onratechange(self, value: str) -> Attribute:
        return Attribute("onratechange", value)

    def onreset(self, value: str) -> Attribute:
        return Attribute("onreset", value)

    def onresize(self, value: str) -> Attribute:
        return Attribute("onresize", value)

    def onscroll(self, value: str) -> Attribute:
        return Attribute("onscroll", value)

    def onsecuritypolicyviolation(self, value: str) -> Attribute:
        return Attribute("onsecuritypolicyviolation", value)

    def onseeked(self, value: str) -> Attribute:
        return Attribute("onseeked", value)

    def onseeking(self, value: str) -> Attribute:
        return Attribute("onseeking", value)

    def onselect(self, value: str) -> Attribute:
        return Attribute("onselect", value)

    def onslotchange(self, value: str) -> Attribute:
        return Attribute("onslotchange", value)

    def onstalled(self, value: str) -> Attribute:
        return Attribute("onstalled", value)

    def onsubmit(self, value: str) -> Attribute:
        return Attribute("onsubmit", value)

    def onsuspend(self, value: str) -> Attribute:
        return Attribute("onsuspend", value)

    def ontimeupdate(self, value: str) -> Attribute:
        return Attribute("ontimeupdate", value)

    def ontoggle(self, value: str) -> Attribute:
        return Attribute("ontoggle", value)

    def onvolumechange(self, value: str) -> Attribute:
        return Attribute("onvolumechange", value)

    def onwaiting(self, value: str) -> Attribute:
        return Attribute("onwaiting", value)

    def onwheel(self, value: str) -> Attribute:
        return Attribute("onwheel", value)

    def open(self, value: bool = True) -> Attribute:
        return Attribute("open", value)

    def optimum(self, value: str) -> Attribute:
        return Attribute("optimum", value)

    def pattern(self, value: str) -> Attribute:
        return Attribute("pattern", value)

    def ping(self, value: str) -> Attribute:
        return Attribute("ping", value)

    def placeholder(self, value: str) -> Attribute:
        return Attribute("placeholder", value)

    def playsinline(self, value: bool = True) -> Attribute:
        return Attribute("playsinline", value)

    def popover(self, value: Literal["auto", "manual"]) -> Attribute:
        return Attribute("popover", value)

    def poster(self, value: str) -> Attribute:
        return Attribute("poster", value)

    def preload(self, value: Literal["auto", "metadata", "none"]) -> Attribute:
        return Attribute("preload", value)

    def readonly(self, value: bool = True) -> Attribute:
        return Attribute("readonly", value)

    def referrerpolicy(
        self,
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
        self,
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

    def required(self, value: bool = True) -> Attribute:
        return Attribute("required", value)

    def reversed(self, value: bool = True) -> Attribute:
        return Attribute("reversed", value)

    def role(self, value: str) -> Attribute:
        return Attribute("role", value)

    def rows(self, value: int) -> Attribute:
        return Attribute("rows", value)

    def rowspan(self, value: int) -> Attribute:
        return Attribute("rowspan", value)

    def sandbox(
        self,
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

    def scope(self, value: Literal["col", "row", "colgroup", "rowgroup"]) -> Attribute:
        return Attribute("scope", value)

    def selected(self, value: bool = True) -> Attribute:
        return Attribute("selected", value)

    def shape(self, value: Literal["default", "rect", "circle", "poly"]) -> Attribute:
        return Attribute("shape", value)

    def size(self, value: int) -> Attribute:
        return Attribute("size", value)

    def sizes(self, *value: str) -> Attribute:
        return Attribute("sizes", ",".join(value))

    def slot(self, value: str) -> Attribute:
        return Attribute("slot", value)

    def span(self, value: int) -> Attribute:
        return Attribute("span", value)

    def spellcheck(self, value: Literal["true", "false"] | bool = True) -> Attribute:
        return Attribute("spellcheck", value)

    def src(self, value: str) -> Attribute:
        return Attribute("src", value)

    def srcdoc(self, value: str) -> Attribute:
        return Attribute("srcdoc", value)

    def srclang(self, value: str) -> Attribute:
        return Attribute("srclang", value)

    def srcset(self, *value: str) -> Attribute:
        return Attribute("srcset", ",".join(value))

    def start(self, value: str) -> Attribute:
        return Attribute("start", value)

    def step(self, value: int | float | Literal["any"]) -> Attribute:
        return Attribute("step", value)

    def style(self, value: str) -> Attribute:
        return Attribute("style", value)

    def tabindex(self, value: int) -> Attribute:
        return Attribute("tabindex", value)

    def target(
        self,
        value: Literal["_self", "_blank", "_parent", "_top"] | str,
    ) -> Attribute:
        return Attribute("target", value)

    def title(self, value: str) -> Attribute:
        return Attribute("title", value)

    def translate(self, value: Literal["yes", "no"]) -> Attribute:
        return Attribute("translate", value)

    def type(
        self,
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

    def usemap(self, value: str) -> Attribute:
        return Attribute("usemap", value)

    def value(self, value: str | int | float) -> Attribute:
        return Attribute("value", value)

    def virtualkeyboardpolicy(
        self,
        value: Literal["auto", "manual"] = "auto",
    ) -> Attribute:
        return Attribute("virtualkeyboardpolicy", value)

    def writingsuggestions(self, value: bool = True) -> Attribute:
        return Attribute("writingsuggestions", value)

    def width(self, value: int | str) -> Attribute:
        return Attribute("width", value)

    def wrap(self, value: Literal["hard", "soft", "off"]) -> Attribute:
        return Attribute("wrap", value)
