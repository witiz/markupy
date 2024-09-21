from jinja2 import Template

from markupy.tag import Li


def test_template_injection() -> None:
    result = Template("<ul>{{ stuff }}</ul>").render(stuff=Li["I am safe!"])
    assert result == "<ul><li>I am safe!</li></ul>"
