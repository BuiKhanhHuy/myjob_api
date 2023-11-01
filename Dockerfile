# syntax=docker/dockerfile:1

FROM python:3.10-alpine

WORKDIR /myjob_api
COPY requirements.txt requirements.txt
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]