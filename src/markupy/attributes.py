import sys

from ._private.attributes import HtmlAttributes

at: HtmlAttributes = HtmlAttributes(__name__)
sys.modules[__name__] = at

accept = at.accept
accept_charset = at.accept_charset
accesskey = at.accesskey
action = at.action
align = at.align
allow = at.allow
alt = at.alt
as_ = at.as_
async_ = at.async_
autocapitalize = at.autocapitalize
autocomplete = at.autocomplete
autofocus = at.autofocus
autoplay = at.autoplay
background = at.background
bgcolor = at.bgcolor
border = at.border
capture = at.capture
charset = at.charset
checked = at.checked
cite = at.cite
class_ = at.class_
color = at.color
cols = at.cols
colspan = at.colspan
content = at.content
contenteditable = at.contenteditable
controls = at.controls
coords = at.coords
crossorigin = at.crossorigin
csp = at.csp
data = at.data
datetime = at.datetime
decoding = at.decoding
default = at.default
defer = at.defer
dir = at.dir
dirname = at.dirname
disabled = at.disabled
download = at.download
draggable = at.draggable
enctype = at.enctype
enterkeyhint = at.enterkeyhint
elementtiming = at.elementtiming
for_ = at.for_
form = at.form
formaction = at.formaction
formenctype = at.formenctype
formmethod = at.formmethod
formnovalidate = at.formnovalidate
formtarget = at.formtarget
headers = at.headers
height = at.height
hidden = at.hidden
high = at.high
href = at.href
hreflang = at.hreflang
http_equiv = at.http_equiv
id = at.id
inputmode = at.inputmode
integrity = at.integrity
ismap = at.ismap
itemprop = at.itemprop
kind = at.kind
label = at.label
lang = at.lang
loading = at.loading
list = at.list
loop = at.loop
low = at.low
max = at.max
maxlength = at.maxlength
media = at.media
method = at.method
min = at.min
minlength = at.minlength
multiple = at.multiple
muted = at.muted
name = at.name
novalidate = at.novalidate
onabort = at.onabort
onautocomplete = at.onautocomplete
onautocompleteerror = at.onautocompleteerror
onblur = at.onblur
oncancel = at.oncancel
oncanplay = at.oncanplay
oncanplaythrough = at.oncanplaythrough
onchange = at.onchange
onclick = at.onclick
onclose = at.onclose
oncontextmenu = at.oncontextmenu
oncuechange = at.oncuechange
ondblclick = at.ondblclick
ondrag = at.ondrag
ondragend = at.ondragend
ondragenter = at.ondragenter
ondragexit = at.ondragexit
ondragleave = at.ondragleave
ondragover = at.ondragover
ondragstart = at.ondragstart
ondrop = at.ondrop
ondurationchange = at.ondurationchange
onemptied = at.onemptied
onended = at.onended
onerror = at.onerror
onfocus = at.onfocus
onformdata = at.onformdata
oninput = at.oninput
oninvalid = at.oninvalid
onkeydown = at.onkeydown
onkeypress = at.onkeypress
onkeyup = at.onkeyup
onload = at.onload
onloadeddata = at.onloadeddata
onloadedmetadata = at.onloadedmetadata
onloadstart = at.onloadstart
onmousedown = at.onmousedown
onmouseenter = at.onmouseenter
onmouseleave = at.onmouseleave
onmousemove = at.onmousemove
onmouseout = at.onmouseout
onmouseover = at.onmouseover
onmouseup = at.onmouseup
onpause = at.onpause
onplay = at.onplay
onplaying = at.onplaying
onprogress = at.onprogress
onratechange = at.onratechange
onreset = at.onreset
onresize = at.onresize
onscroll = at.onscroll
onsecuritypolicyviolation = at.onsecuritypolicyviolation
onseeked = at.onseeked
onseeking = at.onseeking
onselect = at.onselect
onslotchange = at.onslotchange
onstalled = at.onstalled
onsubmit = at.onsubmit
onsuspend = at.onsuspend
ontimeupdate = at.ontimeupdate
ontoggle = at.ontoggle
onvolumechange = at.onvolumechange
onwaiting = at.onwaiting
onwheel = at.onwheel
open = at.open
optimum = at.optimum
pattern = at.pattern
ping = at.ping
placeholder = at.placeholder
playsinline = at.playsinline
popover = at.popover
poster = at.poster
preload = at.preload
readonly = at.readonly
referrerpolicy = at.referrerpolicy
rel = at.rel
required = at.required
reversed = at.reversed
role = at.role
rows = at.rows
rowspan = at.rowspan
sandbox = at.sandbox
scope = at.scope
selected = at.selected
shape = at.shape
size = at.size
sizes = at.sizes
slot = at.slot
span = at.span
spellcheck = at.spellcheck
src = at.src
srcdoc = at.srcdoc
srclang = at.srclang
srcset = at.srcset
start = at.start
step = at.step
style = at.style
tabindex = at.tabindex
target = at.target
title = at.title
translate = at.translate
type = at.type
usemap = at.usemap
value = at.value
virtualkeyboardpolicy = at.virtualkeyboardpolicy
writingsuggestions = at.writingsuggestions
width = at.width
wrap = at.wrap

__all__ = [
    "accept",
    "accept_charset",
    "accesskey",
    "action",
    "align",
    "allow",
    "alt",
    "as_",
    "async_",
    "autocapitalize",
    "autocomplete",
    "autofocus",
    "autoplay",
    "background",
    "bgcolor",
    "border",
    "capture",
    "charset",
    "checked",
    "cite",
    "class_",
    "color",
    "cols",
    "colspan",
    "content",
    "contenteditable",
    "controls",
    "coords",
    "crossorigin",
    "csp",
    "data",
    "datetime",
    "decoding",
    "default",
    "defer",
    "dir",
    "dirname",
    "disabled",
    "download",
    "draggable",
    "enctype",
    "enterkeyhint",
    "elementtiming",
    "for_",
    "form",
    "formaction",
    "formenctype",
    "formmethod",
    "formnovalidate",
    "formtarget",
    "headers",
    "height",
    "hidden",
    "high",
    "href",
    "hreflang",
    "http_equiv",
    "id",
    "inputmode",
    "integrity",
    "ismap",
    "itemprop",
    "kind",
    "label",
    "lang",
    "loading",
    "list",
    "loop",
    "low",
    "max",
    "maxlength",
    "media",
    "method",
    "min",
    "minlength",
    "multiple",
    "muted",
    "name",
    "novalidate",
    "onabort",
    "onautocomplete",
    "onautocompleteerror",
    "onblur",
    "oncancel",
    "oncanplay",
    "oncanplaythrough",
    "onchange",
    "onclick",
    "onclose",
    "oncontextmenu",
    "oncuechange",
    "ondblclick",
    "ondrag",
    "ondragend",
    "ondragenter",
    "ondragexit",
    "ondragleave",
    "ondragover",
    "ondragstart",
    "ondrop",
    "ondurationchange",
    "onemptied",
    "onended",
    "onerror",
    "onfocus",
    "onformdata",
    "oninput",
    "oninvalid",
    "onkeydown",
    "onkeypress",
    "onkeyup",
    "onload",
    "onloadeddata",
    "onloadedmetadata",
    "onloadstart",
    "onmousedown",
    "onmouseenter",
    "onmouseleave",
    "onmousemove",
    "onmouseout",
    "onmouseover",
    "onmouseup",
    "onpause",
    "onplay",
    "onplaying",
    "onprogress",
    "onratechange",
    "onreset",
    "onresize",
    "onscroll",
    "onsecuritypolicyviolation",
    "onseeked",
    "onseeking",
    "onselect",
    "onslotchange",
    "onstalled",
    "onsubmit",
    "onsuspend",
    "ontimeupdate",
    "ontoggle",
    "onvolumechange",
    "onwaiting",
    "onwheel",
    "open",
    "optimum",
    "pattern",
    "ping",
    "placeholder",
    "playsinline",
    "popover",
    "poster",
    "preload",
    "readonly",
    "referrerpolicy",
    "rel",
    "required",
    "reversed",
    "role",
    "rows",
    "rowspan",
    "sandbox",
    "scope",
    "selected",
    "shape",
    "size",
    "sizes",
    "slot",
    "span",
    "spellcheck",
    "src",
    "srcdoc",
    "srclang",
    "srcset",
    "start",
    "step",
    "style",
    "tabindex",
    "target",
    "title",
    "translate",
    "type",
    "usemap",
    "value",
    "virtualkeyboardpolicy",
    "writingsuggestions",
    "width",
    "wrap",
]
