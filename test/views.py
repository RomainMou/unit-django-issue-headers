from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # breakpoint()
    return HttpResponse("Hello, HTTP_ASCIITEST is ascii? " + str(request.META.get("HTTP_ASCIITEST").isascii()) + "\n")
