# Mastering elements

## Importing elements

HTML elements are imported directly from the `markupy.elements` module as their name using the CapitalizedCase syntax. Although HTML elements are usually spelled in lower case, using CapitalizedCase in markupy avoids naming conflicts with your own variables and makes it easier to distinguish markupy tags vs other parts of your code.

```python title="Importing elements"
>>> from markupy.elements import Div
>>> print(Div)
<div></div>
```

You can import elements individually as shown above, or you can use an alias to dynamically invoke elements as you need them:

```python title="Importing elements with alias"
>>> from markupy.elements as el
>>> print(el.Div)
<div></div>
>>> print(el.Input)
<input>
```

## Element content

Content of elements is specified using square brackets `[]` syntax on an element.
Let's take our example from above and specify content for our `div`:

```python title="Div content"
>>> from markupy.elements import Div
>>> print(Div["Hello World!"])
<div>Hello World!</div>
```

Content can be strings, ints, lists, other elements, etc...
Basically, whatever can be iterated and/or stringified is a valid content.
And you are not limited to just one child, can be as meny as you want:

```python title="Nested elements"
>>> from markupy.elements import Div, H1
>>> print(Div[H1["Lorem ipsum"], "Hello World!"])
<div><h1>Lorem ipsum</h1>Hello World!</div>
```

!!! note "Don't forget to close your tags"

    Another main advantage of the markupy syntax over raw HTML is that you don't have to repeat the tag name to close an element. Of course you still need to close your tags with a closing bracket `]` but this is much more straightforward and your IDE should help you matching/indenting them fairly easily.


## Element attributes

HTML attributes are specified by using parenthesis `()` syntax on an element.

```python title="Element attributes"
>>> from markupy.elements import Div
>>> print(Div(id="container", style="color:red"))
<div id="container" style="color:red"></div>
```

They can be specified in different ways.

### Elements without attributes

For elements that you do not want attributes, they can be specified by just the element itself:

```python
>>> from markupy.elements import Hr
>>> print(Hr)
<hr>
```

### Keyword attributes

Attributes can be specified via keyword arguments, also known as kwargs:

```python
>>> from markupy.elements import Img
>>> print(Img(src="picture.jpg"))
<img src="picture.jpg">
```

In Python, some names such as `class` and `for` are reserved and cannot be used as keyword arguments. Instead, they can be specified as `class_` or `for_` when using keyword arguments:

```python
>>> from markupy.elements import Label
>>> print(Label(for_="myfield"))
<label for="myfield"></label>
```

Attributes that contains dashes `-` can be specified by using underscores:

```python
>>> from markupy.elements import Form
>>> print(Form(hx_post="/foo"))
<form hx-post="/foo"></form>
```

### Selector string shorthand for id and class

Defining `id` and `class` attributes is common when writing HTML. A string shorthand
that looks like a CSS selector can be used to quickly define id and classes:

```python title="Define id"
>>> from markupy.elements import Div
>>> print(Div("#myid"))
<div id="myid"></div>
```

```python title="Define multiple classes"
>>> from markupy.elements import Div
>>> print(Div(".foo.bar"))
<div class="foo bar"></div>
```

```python title="Combining both id and classes"
>>> from markupy.elements import Div
>>> print(Div("#myid.foo.bar"))
<div id="myid" class="foo bar"></div>
```

!!! warning "Selector string format"

    The selector string should begin with the `#id` if present, then followed by `.classes` definition.

### Dict attributes

Attributes can also be specified as a `dict`. This is useful when using
attributes that are reserved Python keywords (like `for` or `class`), when the
attribute name contains special characters or when you want to define attributes
dynamically.

```python title="Using Alpine.js with @-syntax (shorthand for x-on)"
>>> from markupy.elements import Button
>>> print(Button({"@click.shift": "addToSelection()"}))
<button @click.shift="addToSelection()"></button>
```

```python title="Using an attribute with a reserved keyword"
>>> from markupy.elements import Label
>>> print(Label({"for": "myfield"}))
<label for="myfield"></label>
```

### Object attributes

Finally there is one last way to define attributes and it is very powerful, it is called "object attributes", athough it's very transparent as a user since you're only ever calling functions that build those objects for you.

```python title="Using object attributes"
>>> from markupy import attributes as at
>>> from markupy.elements import Input
>>> print(Input(at.id("myid"), at.tabindex(3), at.disabled(True)))
<input id="myid" tabindex="3" disabled>
```

There are multiple benefits of defining attributes this way:

- Suggestion: your IDE will suggest what attributes you can use
- Type hinting: attributes all have their own type (`disabled` is `bool`, `maxlength` is `int`, etc...)
- Autocompletion: for attributes that take pre-definied set of values, you will be able to autocomplete them, avoiding the risk of forgetting or mistyping the correct values
- Helper functions for some attributes like `class_()` that can take multiple input types (`str`, `list`, `dict`) for commodity

Finally, custom object attributes can be defined in several ways:

- If attribute is a valid python identifier, just do `at.foo_bar("baz")`
- Otherwise, you can pass any arbitrary string by constructing an attribute object and pass it a name and a value: `Attribute("@foo:bar", "baz")`


### Combining different types of attributes

Attributes via id/class selector shorthand, dictionary, object and keyword attributes can be combined and used simultaneously:

```python title="Specifying attribute via multiple arguments"
>>> from markupy import attributes as attr
>>> from markupy.elements import Label
>>> print(Label("#myid.foo.bar", {"for": "somefield"}, at.tabindex(-1), name="myname"))
<label id="myid" class="foo bar" for="somefield" tabindex="-1" name="myname"></label>
```

!!! warning "Order is important"

    When combining multiple attribute definition methods, it's important to respect the order between them:
    
    1. **selector id/class string** (optional, at most one)
    2. **dictionary attributes** (optional, at most one)
    3. **object attributes** (optional, unlimited)
    4. **keyword attributes** (optional, unlimited)