import time

import django
from django.conf import settings
from django.template import Context
from django.template import Template as DjangoTemplate
from htpy import table, tbody, td, th, thead, tr
from jinja2 import Template as JinjaTemplate

from markupy.tag import Table, Tbody, Td, Th, Thead, Tr

settings.configure(
    TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates"}]
)
django.setup()

django_jinja_template = """
<table>
    <thead><tr><th>Row #</th></tr></thead>
    <tbody>
        {% for row in rows %}
        <tr><td>{{ row }}</td></tr>
        {% endfor %}
    </tbody>
</table>
"""


tests = [
    (
        "markupy",
        lambda rows: str(
            Table()[
                Thead()[Tr()[Th()["Row #"]]],
                Tbody()[(Tr(class_="row")[Td("#test.cls")[str(row)]] for row in rows)],
            ]
        ),
    ),
    (
        "markupy_simple",
        lambda rows: str(
            Table()[
                Thead[Tr[Th["Row #"]]],
                Tbody[(Tr[Td[str(row)]] for row in rows)],
            ]
        ),
    ),
    (
        "htpy",
        lambda rows: str(
            table()[
                thead()[tr()[th()["Row #"]]],
                tbody()[(tr(class_="row")[td("#test.cls")[str(row)]] for row in rows)],
            ]
        ),
    ),
    (
        "htpy_simple",
        lambda rows: str(
            table[
                thead[tr[th["Row #"]]],
                tbody[(tr[td[str(row)]] for row in rows)],
            ]
        ),
    ),
    (
        "django",
        lambda rows: DjangoTemplate(django_jinja_template).render(
            Context({"rows": rows})
        ),
    ),
    ("jinja2", lambda rows: JinjaTemplate(django_jinja_template).render(rows=rows)),
]
rows = list(range(50_000))

for name, func in tests:
    start = time.perf_counter()
    output = func(rows)
    result = time.perf_counter() - start
    print(f"{name}: {result} seconds")
