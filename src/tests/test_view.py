from markupy import View


def test_empty_view() -> None:
    assert str(View()) == ""
