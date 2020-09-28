FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

RUN apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip


WORKDIR /app

RUN pip install -r Flask==1.1.2 redis==3.5.3

COPY fibonacci_service.py /app/fibonacci_service.py
COPY generator.py /app/generator.py

CMD python3 fibonacci_service.py
