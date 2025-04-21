from markupy import attributes as attr
from markupy import elements as el

print(el.H1(attr.disabled(), attr.sandbox("allow-downloads", "allow-forms")))
