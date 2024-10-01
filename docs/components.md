# Components

Although markupy intend to remain a generic library to allow you generate HTML, it also provides a powerful support for components in order to build reusable chunks of HTML.

## Create reusable fragments with components

### Building your first component

Building a component is done by subclassing the built-in `Component` abstract class and implementing the most basic `render()` instance method that defines your component structure:

```python
from markupy import Component, Node

class MyComponent(Component):
    def render(self) -> Node:
        return "My first component"
```

And then to generate the actual HTML for this component, you just need to instantiate it and make it into a `str`:

```python
>>> print(str(MyComponent()))
My first component
```

This very basic component only renders text for now. 

### Including elements into a component

Note that the component `render()` method can return any valid `Node`, meaning that any valid element child (including elements themselves) can be rendered as part of a component.

Let's create a more useful component that renders a [Boostrap card](https://getbootstrap.com/docs/5.3/components/card/):

```python
from markupy import Component, Node
from markupy.tag import Div, H5, P

class CardComponent(Component):
    def render(self) -> Node:
        return Div(".card")[
            Div(".card-body")[
                H5(".card-title")[
                    "Card title"
                ],
                P(".card-text")[
                    "This is my card's content."
                ],
            ]
        ]
```

See how this can save you from repeating a lot of code?
But we're not there yet, because right now our card always has the same title and content.
Time to keep improving our component.

### Pass data to a components with constructor

Let's make our card data dynamic by adding a constructor to our component. Let's say our card is in charge of displaying a `Post` object:

```python
from markupy import Component, Node
from markupy.tag import Div, H5, P

class CardComponent(Component):
    def __init__(self, *, post: Post) -> None:
        self.post = post

    def render(self) -> Node:
        return Div(".card")[
            Div(".card-body")[
                H5(".card-title")[
                    self.post.title
                ],
                P(".card-text")[
                    self.post.description
                ],
            ]
        ]
```

We could then call our component like so:

```python
>>> CardComponent(post=my_post)
```

### Components in components

Usually, cards are displayed as part of a collection. Let's say we have a blog that is managing a list of posts, let's create a new component that would be in charge of displaying a list of cards:

```python
from markupy import Component, Node
from markupy.tag import Div, H5, P

class CardListComponent(Component):
    def __init__(self, *, posts: list[Post]) -> None:
        self.posts = posts

    def render(self) -> Node:
        return Div(".card-group")[
            (CardComponent(post=post) for post in self.posts)
        ]
```

And that's it, we are looping over a list of posts to generate card components that are added as children of another component. Displaying a list of posts as cards is now super easy:

```python
>>> CardListComponent(posts=my_posts)
```

## Using components to define layouts

