# Overview

markupy is a plain Python alternative to traditional templates engines for generating HTML code.

**Writing this code in Python with markupy...**

```python
# Import "tags" like they were regular Python objects
from markupy.tag import A, Body, Head, Html, Li, P, Title, Ul

menu = [("Home", "/"), ("About us", "/about"), ("Contact", "/contact")]
print(
    Html[
        Head[Title["My website"]],
        Body[
            P["Table of contents:"],
            Ul(".menu")[(Li[A(href=url)[title]] for title, url in menu)],
        ],
    ]
)
```

**...will generate this HTML:**

```html
<!doctype html>
<html>
  <head>
    <title>My website</title>
  </head>
  <body>
    <p>Table of contents:</p>
    <ul class="menu">
      <li><a href="/">Home</a></li>
      <li><a href="/about">About us</a></li>
      <li><a href="/contact">Contact</a></li>
    </ul>
  </body>
</html>
```

Seems interesting? Try it by yourself with our [online html2markupy converter](https://html2markupy.witiz.com).

## Motivation

Like most Python web developers, we have relied on template engines (Jinja, Django, ...) since forever to generate HTML on the server side. Although this is fine for simple needs, when your site grows bigger, you might start facing some issues:

- More an more Python code get put into unreadable and untestable macros

- Extends and includes make it very hard to track required parameters

- Templates are very permissive regarding typing making it more error prone

If this is you struggling with templates, then you should definitely give markupy a try!

## Inspiration

markupy started as a fork of [htpy](https://htpy.dev). Even though the two projects are still conceptually very similar, we started markupy in order to support a slightly different syntax to optimize readability, reduce risk of conflicts with variables, and better support for non native html attributes syntax as python kwargs. On top of that, markupy provides a first class support for class based components.

## Key Features

- **Leverage static types:** Use [mypy](https://mypy.readthedocs.io/en/stable/) or [pyright](https://github.com/microsoft/pyright) to type check your code.

- **Great debugging:** Avoid cryptic stack traces from templates. Use your favorite Python debugger.

- **Easy to extend:** There is no special way to define template tags/filters. Just call regular functions.

- **Works with existing Python web framework:** Works great with Django, Flask or any other Python web framework!

- **Works great with htmx:** markupy makes for a great experience when writing server rendered partials/components.

- **Create reusable components:** Define components, snippets, complex layouts/pages as regular Python variables or functions.

- **Familiar concepts from React:** React helped make it popular writing HTML with a programming language. markupy uses a lot of similar constructs.

## Philosophy

markupy generates HTML elements and attributes and provide a few helpers.

markupy does not enforce any particular pattern or style to organize
your pages, components and layouts. That does not mean that markupy cannot be used
to build sophisticated web pages or applications.

Rather the opposite: you are encouraged the leverage the power of Python to
structure your project. Use modules, classes, functions, decorators, list
comprehension, generators, conditionals, static typing and any other feature of
Python to organize your components. This gives you a lot of power and makes markupy
scale from a small one file project to bigger applications.


## Installation

[markupy is available on PyPI](https://pypi.org/project/markupy/). You may install the latest version using pip:

```
pip install markupy
```

## Documentation

The full documentation is available at [markupy.witiz.com](https://markupy.witiz.com):

- [Usage](https://markupy.witiz.com/usage/)
- [Components](https://markupy.witiz.com/components/)
- [html2markupy](https://markupy.witiz.com/html2markupy/)
- [Integrating with Flask](https://markupy.witiz.com/flask/)
- [Integrating with Starlette](https://markupy.witiz.com/starlette/)
- [Integrating with Django](https://markupy.witiz.com/django/)