# type: ignore
from django.conf import settings
from django.http import HttpResponse
from django.urls import path

from markupy import tag

# --- Django minimal config ---
settings.configure(
    ROOT_URLCONF=__name__,
)


# --- The view ---
def hello_world(request):
    return HttpResponse(tag.H1(".title")["django"])


# --- URL config ---
urlpatterns = [
    path("hello/", hello_world),
]


def test_hello_world_response(client):
    response = client.get("/hello/")
    assert response.status_code == 200
    assert response.content.decode() == """<h1 class="title">django</h1>"""
