FROM python:3.7

WORKDIR /usr/src/fastapi

COPY ./app ./app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt