FROM ubuntu:18.04

MAINTAINER charlie4fun

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

RUN apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY fib_app.py /app/fib_app.py
COPY combi_finder.py /app/combi_finder.py

CMD python3 fib_app.py
