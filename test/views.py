from django.shortcuts import render
from django.http import HttpResponse
import time

def index(request):
    return HttpResponse("Hi.🙂\n")

def ascii(request):
    test_value = request.META.get("HTTP_ASCIITEST")
    response = "'{value}' ({len}) {ascii}\n".format(
       value=test_value,
       len=len(test_value),
       ascii='[ascii]' if test_value.isascii() else '[non-ascii]'
    )
    return HttpResponse(response)

def timeout(request):
    for i in range(5):
        print(i)
        time.sleep(5)
    return HttpResponse("Graceful shutdown.\n")
