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
        <tr class="row"><td data-value="{{ row }}">{{ row }}</td></tr>
        {% endfor %}
    </tbody>
</table>
"""

rows = list(range(50_000))


def render_markupy() -> str:
    return str(
        Table[
            Thead[Tr[Th["Row #"]]],
            Tbody[(Tr[Td[row]] for row in rows)],
        ]
    )


def render_markupy_attr() -> str:
    return str(
        Table[
            Thead[Tr[Th["Row #"]]],
            Tbody[(Tr(".row")[Td(dataValue=row)[row]] for row in rows)],
        ]
    )


def render_htpy() -> str:
    return str(
        table[
            thead[tr[th["Row #"]]],
            tbody[(tr[td[row]] for row in rows)],
        ]
    )


def render_htpy_attr() -> str:
    return str(
        table[
            thead[tr[th["Row #"]]],
            tbody[(tr(".row")[td(data_value=row)[row]] for row in rows)],
        ]
    )


def render_django() -> str:
    return DjangoTemplate(django_jinja_template).render(Context({"rows": rows}))


def render_jinja() -> str:
    return JinjaTemplate(django_jinja_template).render(rows=rows)


tests = [
    render_markupy,
    render_markupy_attr,
    render_htpy,
    render_htpy_attr,
    render_django,
    render_jinja,
]

for func in tests:
    start = time.perf_counter()
    output = func()
    result = time.perf_counter() - start
    print(f"{func.__name__}: {result} seconds")
