# Integrating with Django

## Returning a markupy Response

markupy elements can be passed directly to `HttpResponse`:

```py title="views.py"
from django.http import HttpResponse
from markupy.tag import H1

def my_view(request):
    return HttpResponse(H1["Hi Django!"])
```

## Using markupy as part of an existing Django template

markupy elements are marked as "safe" and can be injected directly into Django
templates. This can be useful if you want to start using markupy gradually in an
existing template based Django project:

```html title="base.html"
<html>
    <head>
        <title>My Django Site</title>
    </head>
    <body>
        {{ content }}
    </body>
</html>
```

```py title="views.py"
from django.shortcuts import render

from markupy import H1


def index(request):
    return render(request, "base.html", {
        "content": H1["Welcome to my site!"],
    })
```

## Render a Django Form

CSRF token, form widgets and errors can be directly used within markupy elements:

```py title="forms.py"
from django import forms


class MyForm(forms.Form):
    name = forms.CharField()
```

```py title="views.py"
from django.http import HttpRequest, HttpResponse

from .components import my_form_page, my_form_success_page
from .forms import MyForm


def my_form(request: HttpRequest) -> HttpResponse:
    form = MyForm(request.POST or None)
    if form.is_valid():
        return HttpResponse(my_form_success_page())

    return HttpResponse(my_form_page(request, my_form=form))

```

```py title="components.py"
from django.http import HttpRequest
from django.template.backends.utils import csrf_input

from markupy import Component, Node
from markupy.tag import Body, Button, Form, H1, Head, Html, Title

from .forms import MyForm


def base_page(title: str, content: Node) -> Component:
    return Html[
        Head[Title[title]],
        Body[content],
    ]


def my_form_page(request: HttpRequest, *, form: MyForm) -> Component:
    return base_page(
        "My form",
        form(method="post")[
            csrf_input(request),
            form.errors,
            form["name"],
            Button["Submit!"],
        ],
    )


def my_form_success_page() -> Component:
    return base_page(
        "Success!",
        H1["Success! The form was valid!"],
    )
```

## Implement Custom Form Widgets With markupy

You can implement a custom form widget directly with markupy like this:

```py title="widgets.py"
from django.forms import widgets

from markupy.tag import SlInput


class ShoelaceInput(widgets.Widget):
    """
    A form widget using Shoelace's <sl-input> element.
    More info: https://shoelace.style/components/input
    """

    def render(self, name, value, attrs=None, renderer=None):
        return str(SlInput(attrs, name=name, value=value))
```
