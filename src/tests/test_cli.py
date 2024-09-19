from markupy.cli import convert


def test_nested_void() -> None:
    html = """<div><hr></div>"""
    py = """from markupy import Div,Hr\nDiv[Hr]"""
    assert convert(html) == py


def test_empty_element() -> None:
    html = """<div></div>"""
    py = """from markupy import Div\nDiv"""
    assert convert(html) == py


def test_strip() -> None:
    html = """<div>\n</div><div>  \n  </div>"""
    py = """from markupy import Div\nDiv,Div"""
    assert convert(html) == py


def test_doctype() -> None:
    html = """<!doctype html>"""
    py = ""
    assert convert(html) == py


def test_selector() -> None:
    html = """<img id=test class="portait image">"""
    py = """from markupy import Img\nImg("#test.portait.image")"""
    assert convert(html) == py


def test_kwargs() -> None:
    html = """<label for="myfield" style="display:none" http-equiv="x">Hello</label>"""
    py = """from markupy import Label\nLabel(for_="myfield",style="display:none",httpEquiv="x")["Hello"]"""
    assert convert(html) == py


def test_empty_kwargs() -> None:
    html = """<input disabled="" style="">"""
    py = """from markupy import Input\nInput(disabled=True)"""
    assert convert(html) == py


def test_invalid_html() -> None:
    html = """<div>"""
    py = """from markupy import Div\nDiv["""
    assert convert(html) == py


def test_convert() -> None:
    html = """<html><Head><TITLE>Test</title></head><body class=''><h1 id='myid' burger&fries='good' class='title header'>Parse me! <!--My comment--></h1><hr><input class='my-input' disabled value='0' @click.outside.500ms='test' data-test='other' data-url-valid='coucou'><sl-button hx-on:htmx:config-request='attri'>Click!</sl-button></body></html>"""
    py = """from markupy import Body,H1,Head,Hr,Html,Input,SlButton,Title\nHtml[Head[Title["Test"]],Body[H1("#myid.title.header",{"burger&fries":"good"})["Parse me!"],Hr,Input(".my-input",disabled=True,value="0",_click_outside_500ms="test",dataTest="other",dataUrlValid="coucou"),SlButton(hxOn__htmx__configRequest="attri")["Click!"]]]"""
    assert convert(html) == py


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
    py = """from markupy import Body,H1,H2,H3,Li,Ol,P\nBody[H1["{{ heading }}"],P["Welcome to our cooking site, {{ user.name }}!"],H2["Recipe of the Day: {{ recipe.name }}"],P["{{ recipe.description }}"],H3["Instructions:"],Ol["{% for step in recipe.steps %}",Li["{{ step }}"],"{% endfor %}"]]"""
    assert convert(html) == py
