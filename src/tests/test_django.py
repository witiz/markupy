# type: ignore
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from django.urls import path

from markupy import elements

# --- Django minimal config ---
settings.configure(
    ROOT_URLCONF=__name__,
)


# --- The view ---
def render(request):
    return HttpResponse(elements.H1(".title")["render"])


def stream(request):
    return StreamingHttpResponse(iter(elements.H1(".title")["stream"]))


# --- URL config ---
urlpatterns = [
    path("render/", render),
    path("stream/", stream),
]


def test_render(client):
    response = client.get("/render/")
    assert response.status_code == 200
    assert response.content.decode() == """<h1 class="title">render</h1>"""


def test_stream(client):
    response = client.get("/stream/")
    assert response.status_code == 200
    assert (
        b"".join(response.streaming_content).decode()
        == """<h1 class="title">stream</h1>"""
    )
