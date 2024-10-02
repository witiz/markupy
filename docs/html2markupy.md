# Converting HTML to markupy

Maybe you already have a bunch of HTML, or templates that you would like to migrate to markupy.
We got you covered in multiple ways.

## Converting online with the html2markupy website

The simplest way to experiment with markupy and convert your HTML snippets is to use the [online html2markupy converter](https://html2markupy.witiz.com).

The app is powered by markupy itself so you will get the exact same result as the one provided by the below method.

## Converting locally with the built-in html2markupy command


The utility command `html2markupy` ships with `markupy`, and can be used to transform existing html into Python code (markupy!).

```bash
$ html2markupy -h
usage: html2markupy [-h] [--selector | --no-selector] [--tag-prefix | --no-tag-prefix] [input]

positional arguments:
  input                 input HTML from file or stdin

options:
  -h, --help            show this help message and exit
  --selector, --no-selector
                        Use the selector #id.class syntax instead of explicit `id` and `class_` attributes (default: True)
  --tag-prefix, --no-tag-prefix
                        Output mode for imports of markupy elements (default: False)
```

Lets say you have an existing HTML file:

```html title="index.html"
<!DOCTYPE html>
<html lang="en">
<head>
    <title>html2markupy</title>
</head>
<body>
    <header>
        <h1 class="heading">Welcome to html2markupy!</h1>
    </header>
    <main id="container">
        Discover a powerful way to build your HTML pages and components in Python!
    </main>
    <footer>
        Powered by <a href="https://markupy.witiz.com">markupy</a>
    </footer>
</body>
</html>
```

Now, if you run the command, it outputs the corresponding Python code (markupy).

```bash
$ html2markupy index.html
```

```python
from markupy.tag import A,Body,Footer,H1,Head,Header,Html,Main,Title
Html(lang="en")[Head[Title["html2markupy"]],Body[Header[H1(".heading")["Welcome to html2markupy!"]],Main("#container")["Discover a powerful way to build your HTML pages and components in Python!"],Footer["Powered by",A(href="https://markupy.witiz.com")["markupy"]]]]
```

### Piping Input/Stdin Stream

You can also pipe input to markupy:

```bash
$ cat index.html | html2markupy
```

This can be combined with other workflows in the way that you find most suitable.
For example, you might pipe from your clipboard to markupy, and optionally direct the output to a file.


### Formatting the Output

`html2markupy` is by default providing an unformatted output, but you can easily combine it with your preferred formatter (must be installed separately). Below is an example formatting with ruff:

```bash
$ html2markupy index.html | ruff format - 
```

### Command Options

Say you have the following HTML snippet.

```html title="example.html"
<section id="main-section" class="hero is-link">
  <p class="subtitle is-3 is-spaced">Welcome</p>
</section>
```

You can adapt the markupy conversion with a couple of options.

#### Imports management

Some people prefer to `import markupy as tag` instead of importing individual elements `from markupy.tag`.
If this is you, you can use the `--tag-prefix` option to get corresponding output when using `html2markupy`.


=== "--no-tag-prefix (default)"

    ```python
    from markupy import P, Section

    Section("#main-section.hero.is-link")[
        P(".subtitle.is-3.is-spaced")["Welcome"]
    ]
    ```

=== "--tag-prefix"

    ```python
    from markupy import tag

    tag.Section("#main-section.hero.is-link")[
        tag.P(".subtitle.is-3.is-spaced")["Welcome"]
    ]
    ```


#### Explicit ID and Class Kwargs

If you prefer the explicit `id="id", class_="class"` kwargs syntax over the default markupy shorthand `#id.class` syntax, you can get it by passing the `--no-selector` flag.

=== "--selector (default)"

    ```python
    from markupy import P, Section

    Section("#main-section.hero.is-link")[
        P(".subtitle.is-3.is-spaced")["Welcome"]
    ]
    ```

=== "--no-selector"

    ```python
    from markupy import P, Section

    Section(id="main-section", class_="hero is-link")[
        P(class_="subtitle is-3 is-spaced")["Welcome"]
    ]
    ```
