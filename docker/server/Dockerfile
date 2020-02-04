FROM python:3.8-alpine

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.0.0


RUN apk --no-cache add \
     bash \
     build-base \
     curl \
     gcc \
     gettext \
     git \
     libffi-dev \
     linux-headers \
     musl-dev \
     postgresql-dev \
     # Installing `poetry` package manager:
     # https://github.com/python-poetry/poetry
     && pip install "poetry==$POETRY_VERSION"

COPY ./poetry.lock ./pyproject.toml /app/
COPY ./server /app/server
COPY ./asgi.py /app/asgi.py
COPY ./.env /app/.env
COPY ./alembic.ini /app/alembic.ini

WORKDIR /app

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

CMD uvicorn asgi:app
