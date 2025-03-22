from markupy import Fragment
from markupy.tag import I, P


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
