# Django to test to understand headers behaviour in nginx unit

Related to issue : https://github.com/nginx/unit/issues/868

## How to reproduce

This is an almost empty Django project, initialize by following the [Django tutorial](https://docs.djangoproject.com/en/4.2/intro/tutorial01/).
The relevant code is in `test/views.py`, the only thing that is done is:
```
def index(request):
    # breakpoint()
    return HttpResponse("Hello, HTTP_ASCIITEST is ascii? " + str(request.META.get("HTTP_ASCIITEST").isascii()) + "\n")
```

### Test Unit
Build the container : `sudo docker build -f Dockerfiles.unit -t django:unit .`
Run the containers: `sudo docker run -it --rm -p 8000:8000 django:unit`
In another terminal, I use curl to do a requests:
```
romain@grace-hopper:~ » curl --header "ASCIITEST: 1" http://localhost:8000/test/
Hello, HTTP_ASCIITEST is ascii? False
```

We see that the value of `request.META.get("HTTP_DNT")` is not ascii.

### Test Gunicorn
Build the container: `sudo docker build -f Dockerfiles.gunicorn -t django:gunicorn .`
Run the container: `sudo docker run -it --rm -p 8000:8000 django:gunicorn`
In another terminal, I use curl to do a requests:
```
romain@grace-hopper:~ » curl --header "ASCIITEST: 1" http://localhost:8000/test/
Hello, HTTP_ASCIITEST is ascii? True
```

We see that the value of `request.META.get("HTTP_DNT")` is ascii.
