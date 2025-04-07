from typing import Any

from markupy import Component, tag


class MyComponent(Component):
    def __init__(self, **kwargs: Any):
        super().__init__()
        self.kwargs = kwargs

    def render(self):
        return tag.H1(".title.header", **self.kwargs)[self.content()]


print(MyComponent(id="test", dataFoo="bar", class_="main")["Hello"])


class OtherComponent(Component):
    def render(self):
        return tag.H1(".title.header")[self.content()]


print(OtherComponent()["Hello"])


class CoolComponent(Component):
    def __init__(self, **kwargs: Any):
        self.kwargs = kwargs

    def render(self):
        return tag.H1(".title.header", **self.kwargs)[self.content()]


print(CoolComponent(id="test", dataFoo="bar", class_="main")["Hello"])
