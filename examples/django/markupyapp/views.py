from django.http import HttpResponse
from django.shortcuts import render

from markupy.elements import H1, Body, Html


def index(request):
    return HttpResponse(Html[Body[H1["Hi Django!"]]])


def template(request):
    context = {
        "content": H1["This is markupy title!"],
    }
    return render(request, "markupyapp/base.html", context)
