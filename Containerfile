FROM python:3.11.4-slim-buster as build

# set environment variables
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

# install dependencies
RUN pip install --user --upgrade --no-cache-dir pip==22.3.1 && \
    pip install --user --no-cache-dir pipenv==2022.10.25

# install python packages
COPY Pipfile Pipfile.lock .

RUN pipenv requirements --dev > requirements.txt

# copy to a fresh image for reduced size
FROM python:3.11.4-slim-buster

WORKDIR /app
COPY --from=build /app/requirements.txt /app/requirements.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH=/root/.local/bin:$PATH

# copy project
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/src

CMD ["python", "main.py"]
