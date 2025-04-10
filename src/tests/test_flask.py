# type:ignore
import pytest
from flask import Flask

from markupy import tag

app = Flask(__name__)


@app.route("/render")
def render():
    return str(tag.H1(".title")["render"])


@app.route("/stream")
def stream():
    return iter(tag.H1(".title")["stream"])


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_render(client):
    response = client.get("/render")
    assert response.status_code == 200
    assert response.data.decode() == """<h1 class="title">render</h1>"""


def test_stream(client):
    response = client.get("/stream")
    assert response.status_code == 200
    assert response.data.decode() == """<h1 class="title">stream</h1>"""
