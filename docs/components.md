# Components

Although markupy intend to remain a generic library to allow you generate HTML, it also provides a powerful support for components in order to build reusable chunks of HTML.

## Create reusable fragments with components

### Building your first component

Let's start by creating a component that renders a [Boostrap card](https://getbootstrap.com/docs/5.3/components/card/).

#### Components as functions

Building a function component is a simple as returning elements from a regular python function:

```python
def card_component() -> Node:
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

!!! note

    In the rest of the documentation, we will mostly focus on class based components that offer more flexibility with the ability to inherit each other but after all, it's also a matter of taste so feel free to experiment and find what works best for you.


#### Components as classes

Building a class component is done by subclassing the built-in `Component` abstract class and implementing the one required `render()` instance method that defines your component structure.

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

And then to generate the actual HTML for this component, you just need to instantiate it and make it into a `str`:

```python
>>> str(CardComponent())
```

Note that the component `render()` method can return any valid `Node`, meaning that any valid element child (including strings or elements themselves) can be rendered as part of a component.

See how this can save you from repeating a lot of code?
But we're not there yet, because right now our card always has the same title and content.
Time to keep improving our component.

### Pass data to a class component with constructor

Let's make our card data dynamic by adding a constructor to our component. Let's say our card is in charge of displaying a `Post` object:

```python
from markupy import Component, Node
from markupy.tag import Div, H5, P
from my_models import Post

class PostCardComponent(Component):
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

### Components in components

Usually, cards are displayed as part of a collection. Let's say we have a blog that is managing a list of posts, let's create a new component that would be in charge of displaying a list of cards:

```python
from markupy import Component, Node
from markupy.tag import Div, H5, P
from my_models import Post

class PostCardListComponent(Component):
    def __init__(self, *, posts: list[Post]) -> None:
        self.posts = posts

    def render(self) -> Node:
        return Div(".card-group")[
            (PostCardComponent(post=post) for post in self.posts)
        ]
```

And that's it, we are looping over a list of posts to generate card components that are added as children of another component. Displaying a list of posts as cards is now super easy:

```python
>>> str(PostCardListComponent(posts=my_posts))
```

## Using components to define layouts

Another very interesting use for components is to define your pages layouts.

### Implementing a basic layout

Below is a very basic layout that specifies a default head and body, with some placeholders that we can implement when inheriting this layout.

```python
from markupy import Component, Node
from markupy.tag import H1, Body, Footer, Head, Header, Html, Main, Title

class BaseLayout(Component):
    def render_title() -> str:
        return "My website"

    def render_main() -> Node:
        return None

    def render(self) -> Node:
        return Html[
            Head[
                Title[self.render_title()],
            ],
            Body[
                Header(".container")[H1["Welcome!"]],
                Main(".container")[self.render_main()],
                Footer(".container")["© My Company"],
            ],
        ]
```

!!! note

    Here we defined the placeholders as instance methods called render_*. This is just a convention and nothing is enforced in naming them.


### Extending a layout to implement a page

Then when we need to define a specific page, we need to subclass the layout an override the needed placeholders:

```python
from markupy.tag import H2
from my_components import PostCardListComponent
from my_models import Post

class BlogPage(BaseLayout):
    def __init__(self, *, posts:list[Post]) -> None:
        self.posts = posts

    def render_title() -> str:
        return f"Blog | {super().render_title()}"

    def render_main() -> Node:
        return [
            H2["Blog posts"],
            PostCardListComponent(posts=self.posts)
        ]
```

!!! note

    Notice in the `render_title` how we can only partially replace the content from the inherited layout (here we are preprending the default page title with the `Blog | ` value.)

As usual, generating HTML for the page is just a matter of instanciating and converting to `str`:

```python
>>> str(BlogPage(posts=my_posts))
```