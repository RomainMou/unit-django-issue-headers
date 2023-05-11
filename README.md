# Small django to test stuff related to Nginx unit

## How to reproduce

This is an almost empty Django project, initialize by following the [Django tutorial](https://docs.djangoproject.com/en/4.2/intro/tutorial01/).
The relevant code is in `test/views.py`, the only thing that is done is:

Build the containers:
* Unit: `sudo docker build -f Dockerfiles.unit -t django:unit .`
* Gunicorn: `sudo docker build -f Dockerfiles.gunicorn -t django:gunicorn .`


### ASCII
Related to issue : https://github.com/nginx/unit/issues/868
#### Test Unit
Run the containers: `sudo docker run -it --rm -p 8000:8000 django:unit`
In another terminal, I use curl to do a requests:
```
romain@grace-hopper:~ » curl --header "ASCIITEST: 1" http://localhost:8000/test/
Hello, HTTP_ASCIITEST is ascii? False
```

We see that the value of `request.META.get("HTTP_DNT")` is not ascii.

#### Test Gunicorn
Run the container: `sudo docker run -it --rm -p 8000:8000 django:gunicorn`
In another terminal, I use curl to do a requests:
```
romain@grace-hopper:~ » curl --header "ASCIITEST: 1" http://localhost:8000/test/
Hello, HTTP_ASCIITEST is ascii? True
```

We see that the value of `request.META.get("HTTP_DNT")` is ascii.

### Timeout
#### Test Unit
Run the containers: `sudo docker run -it --rm -p 8000:8000 --name django_unit django:unit`
In another terminal, I use curl to do a requests: `romain@grace-hopper:~ » curl http://localhost:8000/test/timeout`
In another terminal, I use docker to ask a graceful shutdown before the end of the processing: `sudo docker stop -t 60 -s 15 django_unit` 

What I see:
In the curl output, we have an error with and empty reply just after the launch of the `docker stop` command:
```
romain@grace-hopper:~ curl http://localhost:8000/test/timeout
curl: (52) Empty reply from serve
```

In the container output, we see two processes killed just after the `docker stop` command, but the processing continue.
At the end the process can't respond to the client because the socket is gone, I guess.
```
0
1
2
2023/05/11 14:29:09 [notice] 1#1 process 44 exited with code 0
2023/05/11 14:29:09 [notice] 1#1 process 45 exited with code 0
3
4
2023/05/11 14:29:23 [warn] 47#47 [unit] sendmsg(11, 311) failed: Broken pipe (32)
2023/05/11 14:29:23 [notice] 46#46 app process 47 exited with code 0
2023/05/11 14:29:23 [alert] 46#46 sendmsg(13, -1, -1, 2) failed (32: Broken pipe)
2023/05/11 14:29:23 [notice] 1#1 process 46 exited with code 0
```

#### Test Gunicorn
Run the containers: `sudo docker run -it --rm -p 8000:8000 --name django_gunicorn django:gunicorn`
In another terminal, I use curl to do a requests: `romain@grace-hopper:~ » curl http://localhost:8000/test/timeout`
In another terminal, I use docker to ask a graceful shutdown before the end of the processing: `sudo docker stop -t 60 -s 15 django_gunicorn` 

What I see:
In the curl output, everything is normal:
```
romain@grace-hopper:~ curl http://localhost:8000/test/timeout
Graceful shutdown.
```

In the container output, we see a log to inform us that the term signal is handle, the process continue, and the answer to the client is correctly sent to the client and then the gunicorn successfuly exited
```
0
1
2
[2023-05-11 14:35:37 +0000] [1] [INFO] Handling signal: term
3
4
[2023-05-11 14:35:55 +0000] [7] [INFO] Worker exiting (pid: 7)
[2023-05-11 14:35:55 +0000] [1] [INFO] Shutting down: Master
```
