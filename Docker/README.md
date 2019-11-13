# Python Flask Dockerized Hello World! Application interfaced by Gunicorn

This is a quite simple app which serves a "Hello World!" page, which
is run by flask interfaced by gunicorn.

## Why interface flask?
* flasks is not a production but a development server
    * it uses Werkzeug's development server
* performs poorly under high load
* If you leave debug mode on and an error pops up, it opens up a shell that allows for arbitrary code to be executed on your server
* It doesn't scale well

The recommended approach is to use a production WSGI server - like gunicorn.
There are two sides involved to responding to a clients HTTP request. The application server and the application handler.
The server handles the connections, receiving the request and sending the response. The application handler takes the request data and acts on it, like crafting a response.

Gunicorn (application handler) will be interfaced by a HAProxy or nginx ingress (application server) in Kubernetes to implement rate limiting and other connection handling. SSL will also be implemented by the server using Letsencrypt.
Directing requests only to healty pods, since we are going to deploy more than 1, will be handled by a kubernetes service.
Flask is configured to only return a simple message, which is sufficient for our usecase. But it could also easily return an index file.

Build the image using the following command

```bash
$ docker build . -t karstensiemer/gunicorn_hello_world:v0.1
```

Flask and gunicorn can be configured via environment variables. There are defaults set inside the Dockerfile, but we can easily overwrite those in Kubernetes later on.
Logging and monitoring are not implemented by choice.
A logshipper like fluentbit should gather the access logs.
And monitoring will be implemented by a statsd sidecar from which the http endpoint will be scraped by prometheus.
