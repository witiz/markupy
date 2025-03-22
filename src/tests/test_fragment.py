from markupy import Fragment
from markupy.tag import Div, I, P, Tr


def test_render_direct() -> None:
    assert str(Fragment["Hello ", None, I["World"]]) == """Hello <i>World</i>"""


def test_render_as_child() -> None:
    assert (
        str(P["Say: ", Fragment["Hello ", None, I["World"]], "!"])
        == """<p>Say: Hello <i>World</i>!</p>"""
    )


def test_render_nested() -> None:
    assert str(Fragment[Fragment["Hel", "lo "], "World"]) == """Hello World"""


def test_render_embedded() -> None:
    assert (
        str(P[Fragment["Good ", I["morning"]], " ", I["World"]])
        == """<p>Good <i>morning</i> <i>World</i></p>"""
    )


def test_safe() -> None:
    assert str(Fragment['>"']) == """&gt;&#34;"""


def test_iter() -> None:
    assert list(Fragment["Hello ", None, I["World"]]) == [
        "Hello ",
        "<i>",
        "World",
        "</i>",
    ]


def test_element() -> None:
    result = Fragment[Div["a"]]
    assert str(result) == "<div>a</div>"


def test_multiple_element() -> None:
    result = Fragment[Tr["a"], Tr["b"]]
    assert str(result) == "<tr>a</tr><tr>b</tr>"


def test_list() -> None:
    result = Fragment[[Tr["a"], Tr["b"]]]
    assert str(result) == "<tr>a</tr><tr>b</tr>"


def test_none() -> None:
    result = Fragment[None]
    assert str(result) == ""


def test_string() -> None:
    result = Fragment["hello!"]
    assert str(result) == "hello!"
