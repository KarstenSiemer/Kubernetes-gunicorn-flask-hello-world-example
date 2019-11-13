FROM python:3.8.0-slim-buster
RUN useradd -ms /bin/bash helloworld
COPY requirements.txt app.py /home/helloworld/app/
WORKDIR /home/helloworld/app/
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean -y
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
USER helloworld
ENV FLASK_PORT=8080
CMD gunicorn -b 0.0.0.0:${WSGI_PORT:-8081} app
