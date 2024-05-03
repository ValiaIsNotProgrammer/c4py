FROM python:3.11 as python-base


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
    poetry install --no-root --with api --without bot

#RUN pip install chromedriver-binary
#ENV PATH="chromedriver-path:${PATH}"

# installing google
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable


COPY ./docker/api/start-web.sh app/start-web.sh
RUN chmod +x app/start-web.sh
RUN pip install chromedriver-binary

COPY ./api/ ./app/api/

#WORKDIR app


