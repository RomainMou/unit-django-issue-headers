from django.shortcuts import render
from django.http import HttpResponse
import time

def index(request):
    return HttpResponse("Hi.🙂\n")

def ascii(request):
    return HttpResponse(
        "Hello, HTTP_ASCIITEST is ascii? " + str(request.META.get("HTTP_ASCIITEST").isascii()) + "\n")

def timeout(request):
    for i in range(5):
        print(i)
        time.sleep(5)
    return HttpResponse("Graceful shutdown.\n")
