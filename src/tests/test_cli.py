import pytest

from markupy._private.html import to_markupy


def test_nested_void() -> None:
    html = """<div><hr></div>"""
    py = """from markupy.tag import Div,Hr\nDiv[Hr]"""
    assert to_markupy(html) == py


def test_empty_element() -> None:
    html = """<div></div>"""
    py = """from markupy.tag import Div\nDiv"""
    assert to_markupy(html) == py


def test_strip() -> None:
    html = """<div>\n</div><div>  \n  </div>"""
    py = """from markupy.tag import Div\n[Div,Div]"""
    assert to_markupy(html) == py


def test_doctype() -> None:
    html = """<!doctype html>"""
    py = ""
    assert to_markupy(html) == py


def test_selector() -> None:
    html = """<img id=test class="portait image">"""
    py = """from markupy.tag import Img\nImg("#test.portait.image")"""
    assert to_markupy(html) == py


def test_kwargs() -> None:
    html = """<label for="myfield" style="display:none" http-equiv="x">Hello</label>"""
    py = """from markupy.tag import Label\nLabel(for_="myfield",style="display:none",httpEquiv="x")["Hello"]"""
    assert to_markupy(html) == py


def test_empty_kwargs() -> None:
    html = """<input disabled="" style="">"""
    py = """from markupy.tag import Input\nInput(disabled=True)"""
    assert to_markupy(html) == py


def test_invalid_html_unclosed() -> None:
    html = """<div>"""
    with pytest.raises(ValueError):
        to_markupy(html)


def test_invalid_html_toomany_closed() -> None:
    html = """<div></div></div>"""
    with pytest.raises(ValueError):
        to_markupy(html)


def test_invalid_html_not_matching() -> None:
    html = """<div></pre>"""
    with pytest.raises(ValueError):
        to_markupy(html)


def test_to_markupy() -> None:
    html = """<html><Head><TITLE>Test</title></head><body class=''><h1 id='myid' burger&fries='good' class='title header'>Parse me! <!--My comment--></h1><hr><input class='my-input' disabled value='0' @click.outside.500ms='test' data-test='other' data-url-valid='coucou'><sl-button hx-on:htmx:config-request='attri'>Click!</sl-button></body></html>"""
    py = """from markupy.tag import Body,H1,Head,Hr,Html,Input,SlButton,Title\nHtml[Head[Title["Test"]],Body[H1("#myid.title.header",{"burger&fries":"good"})["Parse me!"],Hr,Input(".my-input",disabled=True,value="0",_click_outside_500ms="test",dataTest="other",dataUrlValid="coucou"),SlButton(hxOn__htmx__configRequest="attri")["Click!"]]]"""
    assert to_markupy(html) == py


def test_escape() -> None:
    html = """<a href="{{ url_for(".index") }}">Hello</a>"""
    py = """from markupy.tag import A\nA(href="{{ url_for(\\".index\\") }}")["Hello"]"""
    assert to_markupy(html) == py


def test_jinja() -> None:
    html = """
    <body>
    <h1>{{ heading }}</h1>
    <p>Welcome to our cooking site, {{ user.name }}!</p>

    <h2>Recipe of the Day: {{ recipe.name }}</h2>
    <p>{{ recipe.description }}</p>

    <h3>Instructions:</h3>
    <ol>
        {% for step in recipe.steps %}
        <li>{{ step }}</li>
        {% endfor %}
    </ol>
    </body>
    """
    py = """from markupy.tag import Body,H1,H2,H3,Li,Ol,P\nBody[H1["{{ heading }}"],P["Welcome to our cooking site, {{ user.name }}!"],H2["Recipe of the Day: {{ recipe.name }}"],P["{{ recipe.description }}"],H3["Instructions:"],Ol["{% for step in recipe.steps %}",Li["{{ step }}"],"{% endfor %}"]]"""
    assert to_markupy(html) == py


def test_self_closing() -> None:
    html = """<input type="checkbox" />"""
    py = """from markupy.tag import Input\nInput(type="checkbox")"""
    assert to_markupy(html) == py


def test_use_import_tag() -> None:
    html = """<div>hello</div>"""
    py = """from markupy import tag\ntag.Div["hello"]"""
    assert to_markupy(html, use_import_tag=True) == py


def test_use_selector() -> None:
    html = """<div id="myid" class="cls1 cls2">hello</div>"""
    py = """from markupy.tag import Div\nDiv(id="myid",class_="cls1 cls2")["hello"]"""
    assert to_markupy(html, use_selector=False) == py


def test_jinja_block() -> None:
    html = """
    {% block my_name %}
        <div></div>
    {% endblock %}
    """
    py = """from markupy.tag import BlockMyName,Div\nBlockMyName[Div]"""
    assert to_markupy(html) == py
