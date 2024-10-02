# Usage

## Elements

HTML elements are imported directly from the `markupy.tag` module as their name using the CapitalizedCase syntax. Although HTML elements are usually spelled in lower case, using CapitalizedCase in markupy avoids naming conflicts with your own variables and makes it easier to distinguish markupy tags vs other parts of your code.

```python title="Importing elements"
>>> from markupy.tag import Div
>>> print(Div)
<div></div>
```

## Attributes

HTML attributes are specified by using parenthesis `()` syntax on an element.

```python title="Element attributes"
>>> from markupy.tag import Div
>>> print(Div(id="container", style="color:red"))
<div id="container" style="color:red"></div>
```

## Children

Children are specified using square brackets `[]` syntax on an element.
Children can be strings, ints, markup, other elements or lists/iterators.

Elements can be arbitrarily nested:

```python title="Nested elements"
>>> from markupy.tag import Article, Section, P
>>> print(Section[Article[P["Lorem ipsum"]]])
<section><article><p>Lorem ipsum</p></article></section>
```

!!! note "Don't forget to close your tags"

    Another main advantage of the markupy syntax over raw HTML is that you don't have to repeat the tag name to close an element. Of course you still need to close your tags with a closing bracket `]` but this is much more straightforward and your IDE should help you matching/indenting them fairly easily.

### Text/Strings

It is possible to pass a string directly as an element's child:

```python title="Using a string as children"
>>> from markupy.tag import H1
>>> print(H1["Welcome to my site!"])
<h1>Welcome to my site!</h1>
```

Strings are automatically escaped to avoid [XSS vulnerabilities](https://owasp.org/www-community/attacks/xss/).
It is convenient and safe to directly insert variable data via f-strings:

```python
>>> from markupy.tag import H1
>>> user_supplied_name = "bobby </h1>"
>>> print(H1[f"hello {user_supplied_name}"])
<h1>hello bobby &lt;/h1&gt;</h1>
```

### Injecting Markup

If you have HTML markup that you want to insert without further escaping, wrap
it in `Markup` from the [markupsafe](https://markupsafe.palletsprojects.com/)
library. markupsafe is a dependency of markupy and is automatically installed:

```python title="Injecting markup"
>>> from markupy.tag import Div
>>> from markupsafe import Markup
>>> print(Div[Markup("<foo></foo>")])
<div><foo></foo></div>
```

If you are generate [Markdown](https://pypi.org/project/Markdown/) and want to insert it into an element, use `Markup`:

```python title="Injecting generated markdown"
>>> from markdown import markdown
>>> from markupsafe import Markup
>>> from markupy.tag import Div
>>> print(Div[Markup(markdown('# Hi'))])
<div><h1>Hi</h1></div>
```

### Conditional Rendering

Children that evaluate to `True`, `False` and `None` will not be rendered.
Python's `and` and `or` operators will [short-circuit](https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not).
You can use this to conditionally render content with inline `and` and `or`.

```python title="Conditional rendering with a value that may be None"

>>> from markupy.tag import Div, Strong

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
>>> from markupy.tag import Div

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

### Loops / Iterating Over Children

You can pass a list, tuple or generator to generate multiple children:

```python title="Iterate over a generator"
>>> from markupy.tag import Ul, Li
>>> print(Ul[(Li[letter] for letter in "abc")])
<ul><li>a</li><li>b</li><li>c</li></ul>
```

!!! note

    The generator will be lazily evaluated when rendering the element, not
    directly when the element is constructed.

A `list` can be used similar to a [JSX fragment](https://react.dev/reference/react/Fragment):

```python title="Render a list of child elements"
>>> from markupy.tag import Div, Img
>>> my_images = [Img(src="a.jpg"), Img(src="b.jpg")]
>>> print(Div[my_images])
<div><img src="a.jpg"><img src="b.jpg"></div>
```

### Custom Elements / Web Components

[Custom elements / web components](https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements) are HTML elements that contains at least one dash (`-`). Since `-` cannot be used in Python identifiers, here's how you'd write them in markupy:

```python title="Custom elements with CapitalizedCase syntax"
>>> from markupy.tag import MyCustomElement
>>> print(MyCustomElement['hi!'])
<my-custom-element>hi!</my-custom-element>
```

### HTML Doctype

The [HTML5 doctype](https://developer.mozilla.org/en-US/docs/Glossary/Doctype) is automatically prepended to the `<html>` tag:

```python
>>> from markupy.tag import Html
>>> print(Html)
<!doctype html><html></html>
```

### HTML Comments

Since the Python code is the source of the HTML generation, to add a comment to
the code, most of the time regular Python comments (`#`) are used.

If you want to emit HTML comments that will be visible in the browser, you need to initialize a special element whose name is `_`:

```python
>>> from markupy.tag import Div, _
>>> print(Div[_["This is a HTML comment"]])
<div><!--This is a HTML comment--></div>
```

Given that a comment is a `Element`, you can wrap other elements as children:

```python
>>> from markupy.tag import Div, Strong, _
>>> print(Div[_["This is a HTML comment", Strong["Hidden text"]]])
<div><!--This is a HTML comment<strong>Hidden text</strong>--></div>
```

If you need full control over the exact rendering of the comment, you can create
comments or arbitrary text by injecting your own markup. See the [Injecting
Markup](#injecting-markup) section above for details.

## Attributes

HTML attributes are defined by calling the element. They can be specified in a couple of different ways.

### Elements Without Attributes

For elements that do not have attributes, they can be specified by just the element itself:

```python
>>> from markupy.tag import Hr
>>> print(Hr)
<hr>
```

### Keyword Arguments

Attributes can be specified via keyword arguments:

```python
>>> from markupy.tag import Img
>>> print(Img(src="picture.jpg"))
<img src="picture.jpg">
```

In Python, some names such as `class` and `for` are reserved and cannot be used as keyword arguments. Instead, they can be specified as `class_` or `for_` when using keyword arguments:

```python
>>> from markupy.tag import Label
>>> print(Label(for_="myfield"))
<label for="myfield"></label>
```

Attributes that contains dashes `-` can be specified using mixedCase syntax:

```python
>>> from markupy.tag import Form
>>> print(Form(hxPost="/foo"))
<form hx-post="/foo"></form>
```

!!! note "But what about PEP8 ?!"

    Some might argue that using mixedCase for attribute names is not Pythonic. It is not indeed. It's a tradeoff we are doing given the low number of chars available to build valid identifiers in Python and the broad diversity of possible chars that can be used as HTML attributes. Just keep in mind anyway that the vast majority of HTML attributes are single worded lower case.

markupy also allows you to write more complex HTML attributes by using the following conventions:

HTML attribute         | markupy attribute      | HTML to markupy conversion
-----------------------|------------------------|----------------------------
`class="..."`          | `class_="..."`         | trailing underscore `_` is meaningless
`data-value="..."`     | `dataValue="..."`      | `kebab-case` ➜ `mixedCase`
`v-on:click="..."`     | `vOn__click="..."`     | colon `:` ➜ double underscore `__`
`@click="..."`         | `_click="..."`         | leading at `@` ➜ leading underscore `_`
`@click.outside="..."` | `_click_outside="..."` | dot `.` ➜ underscore `_`

Combining all those rules together, you can basically write as python identifiers 95% of HTML attributes used in modern frontend frameworks and libraries such as [htmx](https://htmx.org/), [Alpine.js](https://alpinejs.dev/) or [Vue.js](https://vuejs.org)

### Id/Class selector shorthand

Defining `id` and `class` attributes is common when writing HTML. A string shorthand
that looks like a CSS selector can be used to quickly define id and classes:

```python title="Define id"
>>> from markupy.tag import Div
>>> print(Div("#myid"))
<div id="myid"></div>
```

```python title="Define multiple classes"
>>> from markupy.tag import Div
>>> print(Div(".foo.bar"))
<div class="foo bar"></div>
```

```python title="Combining both id and classes"
>>> from markupy.tag import Div
>>> print(Div("#myid.foo.bar"))
<div id="myid" class="foo bar"></div>
```

!!! warning "Selector string format"

    The selector string should begin with the `#id` if present, then followed by `.classes` definition.

### Attributes as Dict

Attributes can also be specified as a `dict`. This is useful when using
attributes that are reserved Python keywords (like `for` or `class`), when the
attribute name contains special characters or when you want to define attributes
dynamically.

```python title="Using Alpine.js with @-syntax (shorthand for x-on)"
>>> from markupy.tag import Button
>>> print(Button({"@click.shift": "addToSelection()"}))
<button @click.shift="addToSelection()"></button>
```

```python title="Using an attribute with a reserved keyword"
>>> from markupy.tag import Label
>>> print(Label({"for": "myfield"}))
<label for="myfield"></label>
```

### Boolean/Empty Attributes

In HTML, boolean attributes such as `disabled` are considered "true" when they
exist. Specifying an attribute as `True` will make it appear (without a value).
`False` will make it hidden. This is useful and brings the semantics of `bool` to
HTML.

```python title="True bool attribute"
>>> from markupy.tag import Button
>>> print(Button(disabled=True))
<button disabled></button>
```

```python title="False bool attribute"
>>> from markupy.tag import Button
>>> print(Button(disabled=False))
<button></button>
```

### Conditionally Mixing CSS Classes

To make it easier to mix CSS classes, the `class` attribute
accepts a list of class names or a dict. Falsey values will be ignored.

```python
>>> from markupy.tag import Button
>>> is_primary = True
>>> print(Button(class_=["btn", {"btn-primary": is_primary}]))
<button class="btn btn-primary"></button>
>>> is_primary = False
>>> print(Button(class_=["btn", {"btn-primary": is_primary}]))
<button class="btn"></button>
>>>
```

### Combining Modes

Attributes via id/class shorthand, keyword arguments and dictionary can be combined:

```python title="Specifying attribute via multiple arguments"
>>> from htyp import label
>>> print(label("#myid.foo.bar", {'for': "somefield"}, name="myname",))
<label id="myid" class="foo bar" for="somefield" name="myname"></label>
```

!!! warning "Order is important"

    When combining multiple attribute definition methods, it's important to respect the order between them:
    first should come the **selector id/class string**, then **dictionary of attributes** and finally **keyword attributes**.

### Escaping of Attributes

Attributes are always escaped. This makes it possible to pass arbitrary HTML
fragments or scripts as attributes. The output may look a bit obfuscated since
all unsafe characters are escaped but the browser will interpret it correctly:

```python
>>> from markupy.tag import Button
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
>>> from markupy.tag import Ul
>>> from markupsafe import Markup
>>> # This markup may come from another library/template engine
>>> some_markup = Markup("""<li class="bar"></li>""")
>>> print(Ul(dataTemplate=some_markup))
<ul data-template="&lt;li class=&#34;bar&#34;&gt;&lt;/li&gt;"></ul>
```

## Render elements without a parent (orphans)

In some cases such as returning partial content it is useful to render elements
without a parent element. This is useful in HTMX partial responses.

You may use `render_node` to achieve this:

```python title="Render elements without a parent"
>>> from markupy import render_node
>>> from markupy.tag import Tr
>>> print(render_node([Tr["a"], Tr["b"]]))
<tr>a</tr><tr>b</tr>
```

`render_node()` accepts all kinds of `Node` objects.
You may use it to render anything that would normally be a child of another element.

!!! note "Best practice: Only use render_node() to render non-Elements"

    You can render regular elements by using `str()`, e.g. `str(P["hi"])`. While
    `render_node()` would give the same result, it is more straightforward and
    better practice to just use `str()` when rendering a regular element. Only
    use `render_node()` when you do not have a parent element.

## Iterating of the Output

Iterating over a markupy element will yield the resulting contents in chunks as
they are rendered:

```python
>>> from markupy.tag import Ul, Li
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


Just like [render_node()](#render-elements-without-a-parent-orphans), there is
`iter_node()` that can be used when you need to iterate over a list of elements
without a parent:

```python
>>> from markupy import iter_node
>>> from markupy.tag import Li
>>> for chunk in iter_node([Li["a"], Li["b"]]):
...     print(f"got a chunk: {chunk!r}")
...
got a chunk: '<li>'
got a chunk: 'a'
got a chunk: '</li>'
got a chunk: '<li>'
got a chunk: 'b'
got a chunk: '</li>'
```