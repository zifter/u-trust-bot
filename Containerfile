FROM python:3.11.4-slim-buster as build

# set environment variables
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

# install dependencies
RUN pip install --user --upgrade --no-cache-dir pip==22.3.1 && \
    pip install --user --no-cache-dir pipenv==2022.10.25

# install python packages
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --dev --deploy --ignore-pipfile

# copy to a fresh image for reduced size
FROM python:3.11.4-slim-buster
COPY --from=build /root/.local /root/.local

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH=/root/.local/bin:$PATH

# copy project
WORKDIR /app
COPY src src
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

WORKDIR /app/src

ENTRYPOINT ["pipenv", "run"]
