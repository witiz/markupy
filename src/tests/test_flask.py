# type:ignore
import pytest
from flask import Flask

from markupy import View, tag


class MarkupyFlask(Flask):
    # Here we override make_response to be able to return View instances
    # from our routes directly without having to cast them to str()
    def make_response(self, rv):
        if isinstance(rv, View):
            rv = str(rv)
        return super().make_response(rv)


app = MarkupyFlask(__name__)


@app.route("/hello")
def hello_world():
    return tag.H1(".title")["flask"]


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_hello_world(client):
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.data.decode() == """<h1 class="title">flask</h1>"""
