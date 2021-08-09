FROM python:3.7

WORKDIR /usr/src/fastapi

COPY ./app ./app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry install
