# Advanced usage

## Loops and conditions

### Looping / iterating over content

You can pass any iterable such as `list`, `tuple` or `generator` to generate multiple children:

```python title="Iterate over a generator"
>>> from markupy.elements import Ul, Li
>>> print(Ul[(Li[letter] for letter in "abc")])
<ul><li>a</li><li>b</li><li>c</li></ul>
```


A `list` can be used similar to a [JSX fragment](https://react.dev/reference/react/Fragment):

```python title="Render a list of child elements"
>>> from markupy.elements import Div, Img
>>> my_images = [Img(src="a.jpg"), Img(src="b.jpg")]
>>> print(Div[my_images])
<div><img src="a.jpg"><img src="b.jpg"></div>
```
### Conditional rendering

Children that evaluate to `True`, `False` and `None` will not be rendered.
Python's `and` and `or` operators will [short-circuit](https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not).
You can use this to conditionally render content with inline `and` and `or`.

```python title="Conditional rendering with a value that may be None"

>>> from markupy.elements import Div, Strong

# No <strong> tag will be rendered since error is None
>>> error = None
>>> print(Div[error and Strong[error]])
<div></div>

>>> error = "Email address is invalid."
>>> print(Div[error and Strong[error]])
<div><strong>Email address is invalid.</strong></div>

# Inline if/else can also be used:
>>> print(Div[Strong[error] if error else None])
<div><strong>Email address is invalid.</strong></div>
```

```python title="Conditional rendering based on a bool variable"
>>> from markupy.elements import Div

>>> is_allowed = True
>>> print(Div[is_allowed and "Access granted!"])
<div>Access granted!</div>
>>> print(Div[is_allowed or "Access denied!"])
<div></div>

>>> is_allowed = False
>>> print(Div[is_allowed and "Access granted!"])
<div></div>
>>> print(Div[is_allowed or "Access denied!"])
<div>Access denied</div>
```

## String escaping

### Element content escaping

Element contents are automatically escaped to avoid [XSS vulnerabilities](https://owasp.org/www-community/attacks/xss/).

```python title="String escaping in action"
>>> from markupy.elements import H1
>>> user_supplied_name = "l33t </h1>"
>>> print(H1[f"hello {user_supplied_name}"])
<h1>hello l33t &lt;/h1&gt;</h1>
```

!!! warning "An exception for `script` and `style` tags"

    Script and style tags are special because they usually expect their content to be respectively javascript and css code. In order for code to work properly, `Script` and `Style` child nodes will not be automatically escaped. Keep in mind that you will need to escape sensitive values yourself inside these 2 tags. 


If you have HTML markup that you want to insert without further escaping, wrap
it in `Markup` from the [markupsafe](https://markupsafe.palletsprojects.com/)
library. markupsafe is a dependency of markupy and is automatically installed:

```python title="Injecting markup"
>>> from markupy.elements import Div
>>> from markupsafe import Markup
>>> print(Div[Markup("<foo></foo>")])
<div><foo></foo></div>
```

If you are generating [Markdown](https://pypi.org/project/Markdown/) and want to insert it into an element, use `Markup`:

```python title="Injecting generated markdown"
>>> from markdown import markdown
>>> from markupsafe import Markup
>>> from markupy.elements import Div
>>> print(Div[Markup(markdown('# Hi'))])
<div><h1>Hi</h1></div>
```

### Element attributes escaping

Attributes are always escaped. This makes it possible to pass arbitrary HTML
fragments or scripts as attributes. The output may look a bit obfuscated since
all unsafe characters are escaped but the browser will interpret it correctly:

```python
>>> from markupy.elements import Button
>>> print(Button(id="example", onclick="let name = 'bob'; alert('hi' + name);")["Say hi"])
<button onclick="let name = &#39;bob&#39;; alert(&#39;hi&#39; + name);">Say hi</button>
```

In the browser, the parsed attribute as returned by
`document.getElementById("example").getAttribute("onclick")` will be the
original string `let name = 'bob'; alert('hi' + name);`.

Escaping will happen whether or not the value is wrapped in `markupsafe.Markup`
or not. This may seem confusing at first but is useful when embedding HTML
snippets as attributes:

```python title="Escaping of Markup"
>>> from markupy.elements import Ul
>>> from markupsafe import Markup
>>> # This markup may come from another library/template engine
>>> some_markup = Markup("""<li class="bar"></li>""")
>>> print(Ul(dataTemplate=some_markup))
<ul data-template="&lt;li class=&#34;bar&#34;&gt;&lt;/li&gt;"></ul>
```

## Special elements

### Custom elements / Web components

[Custom elements / web components](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements) are HTML elements that contains at least one dash (`-`). Since `-` cannot be used in Python identifiers, here's how you'd write them in markupy:

```python title="Custom elements with CapitalizedCase syntax"
>>> from markupy.elements import MyCustomElement
>>> print(MyCustomElement['hi!'])
<my-custom-element>hi!</my-custom-element>
```

### HTML doctype

The [HTML5 doctype](https://developer.mozilla.org/en-US/docs/Glossary/Doctype) is automatically prepended to the `<html>` tag:

```python
>>> from markupy.elements import Html
>>> print(Html)
<!doctype html><html></html>
```

### HTML comments

Since the Python code is the source of the HTML generation, to add a comment to
the code, most of the time regular Python comments (`#`) are used.

If you want to emit HTML comments that will be visible in the browser, you need to initialize a special element whose name is `_`:

```python
>>> from markupy.elements import Div, _
>>> print(Div[_["This is a HTML comment"]])
<div><!--This is a HTML comment--></div>
```

Given that a comment is a `Element`, you can wrap other elements as children:

```python
>>> from markupy.elements import Div, Strong, _
>>> print(Div[_["This is a HTML comment", Strong["Hidden text"]]])
<div><!--This is a HTML comment<strong>Hidden text</strong>--></div>
```


## Advanced attributes

### Boolean attributes

In HTML, boolean attributes such as `disabled` are considered "true" when they
exist. Specifying an attribute as `True` will make it appear (without a value).
`False` will make it hidden. This is useful and brings the semantics of `bool` to
HTML.

```python title="True bool attribute"
>>> from markupy.elements import Button
>>> print(Button(disabled=True))
<button disabled></button>
```

```python title="False bool attribute"
>>> from markupy.elements import Button
>>> print(Button(disabled=False))
<button></button>
```

### 3rd party object attributes libraries

The `markupy.attributes` provides a complete list of HTML5 attributes.
In addition, markupy is exposing all the required APIs for 3rd party libraries to implement object attributes specific to any framework or library.

We will list here any package we might be aware of.

- markupy_htmx


## Streaming / Iterating of the Output

Iterating over a markupy element will yield the resulting contents in chunks as
they are rendered:

```python
>>> from markupy.elements import Ul, Li
>>> for chunk in Ul[Li["a"], Li["b"]]:
...     print(f"got a chunk: {chunk!r}")
...
got a chunk: '<ul>'
got a chunk: '<li>'
got a chunk: 'a'
got a chunk: '</li>'
got a chunk: '<li>'
got a chunk: 'b'
got a chunk: '</li>'
got a chunk: '</ul>'
```

!!! note

    This feature can be leveraged to stream HTML contents by returning a generator instead of a fully generated str. How to integrate this is heavily depending on which framework you are using to power your website.
