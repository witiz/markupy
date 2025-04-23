# type:ignore
import pytest
from flask import Flask, request, stream_with_context

from markupy import elements

app = Flask(__name__)


@app.route("/render")
def render():
    return str(elements.H1(".title")["render"])


@app.route("/stream")
def stream():
    return iter(elements.H1(".title")[request.args["name"]])


@app.route("/stream_context")
def stream_context():
    # Here stream_with_context is useless since the View is build before
    # the streaming starts and context is no longer needed
    return stream_with_context(elements.H1(".title")[request.args["name"]])


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_render(client):
    response = client.get("/render")
    assert response.status_code == 200
    assert response.data.decode() == """<h1 class="title">render</h1>"""


def test_stream(client):
    response = client.get("/stream?name=stream")
    assert response.status_code == 200
    assert response.data.decode() == """<h1 class="title">stream</h1>"""


def test_stream_context(client):
    response = client.get("/stream_context?name=context")
    assert response.status_code == 200
    assert response.data.decode() == """<h1 class="title">context</h1>"""
