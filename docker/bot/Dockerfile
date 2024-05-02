FROM python:3.11-slim as python-base


ENV DJANGO_ENV=${DJANGO_ENV} \
    # python
    PYTHONFAULTHANDLER=1 \
    PYTHONBUFFERD=1 \
    PYTHONHASHSEED=random \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_PERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='var/cache/pypoetry'


RUN pip install poetry==${POETRY_VERSION}

COPY ./poetry.lock ./pyproject.toml ./.env ./app/

RUN cd app/ &&  \
    poetry check &&  \
    poetry install --no-root --with bot --without api

COPY ./docker/bot/start-bot.sh app/start-bot.sh
RUN chmod +x app/start-bot.sh

COPY ./bot/ ./app/bot/
# RUN cd ..