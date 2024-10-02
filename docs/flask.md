# Integrating with Flask

## Basic integration

Rendering markupy elements or components in flask is as easy as return a stringified instance from your routes.

```python
from flask import Flask
from markupy import Component, Node
from markupy.tag import H1

app = Flask(__name__)

@app.route("/page")
def page():
    return str(H1["Hello!"])

class MyComponent(Component):
    def render(self) -> Node:
        return H1["Hello!"]

@app.route("/component")
def component():
    return str(MyComponent())
```

## Avoid casting to str by subclassing Flask

As you saw previously, since Flask doesn't know about our elements or components, we need to convert them to `str` before returning them.

You can avoid that by subclassing `Flask` and overriding the `make_response` method:

```python
from flask import Flask
from markupy import Component

class MarkupyFlask(Flask):
    # Here we override make_response to be able to return Component instances
    # from our routes directly without having to cast them to str()
    def make_response(self, rv):
        if isinstance(rv, Component):
            rv = str(rv)
        return super().make_response(rv)
```

And then our previous example becomes like this (basically we instantiate MarkupyFlask instead of Flask previously and do not need the calls to `str` anymore):

```python

from my_flask import MarkupyFlask
from markupy import Component, Node
from markupy.tag import H1

app = MarkupyFlask(__name__)

@app.route("/page")
def page():
    return H1["Hello!"]

class MyComponent(Component):
    def render(self) -> Node:
        return H1["Hello!"]

@app.route("/component")
def component():
    return MyComponent()
```

## Streaming HTML

Given that markupy elements and components are iterables, you can leverage the power of python generators to stream the response instead of sending it all at once.

Flask supports streaming out of the box ([see docs](https://flask.palletsprojects.com/en/3.0.x/patterns/streaming/)).

!!! note

    The examples below are returning very small and simple content, please be aware that you will only benefit from streaming for large contents.

### Streaming by returning a generator

```python
from flask import Flask, stream_with_context
from markupy import Component, Node
from markupy.tag import H1

app = Flask(__name__)

@app.route("/page")
def page():
    my_element = H1["Hello!"]
    return stream_with_context(chunk for chunk in my_element)

class MyComponent(Component):
    def render(self) -> Node:
        return H1["Hello!"]

@app.route("/component")
def component():
    return stream_with_context(chunk for chunk in MyComponent())
```

### Streaming by subclassing Flask

Same as above, if you prefer a cleaner syntax that will apply streaming to all your routes, we can adapt our `Flask` subclass:

```python
from flask import Flask, stream_with_context
from markupy import Component

class MarkupyStreamFlask(Flask):
    # Here we override make_response to be able to stream Component instances
    # from our routes directly when returning them
    def make_response(self, rv):
        if isinstance(rv, Component):
            rv = stream_with_context(chunk for chunk in rv)
        return super().make_response(rv)
```

And then in your routes:

```python
@app.route("/page")
def page():
    return H1["Hello!"]
```

### Streaming with route decorators

If you prefer to apply this change on a route per route basis, you could also create a decorator that will take care of the component to stream conversion:

```python
from functools import wraps
from flask import stream_with_context
from markupy import Component

def markupy_stream(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        rv = f(*args, **kwargs)
        if isinstance(rv, Component):
            return stream_with_context(chunk for chunk in rv)
        return rv

    return wrapper
```

And then in your routes:

```python
@app.route("/page")
@markupy_stream
def page():
    return H1["Hello!"]
```