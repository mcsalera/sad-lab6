FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt
RUN apk add --update --no-cache postgresql-client

RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev

RUN pip install --no-cache-dir -r requirements.txt
RUN apk del .tmp-build-deps


COPY ./mysite /mysite
WORKDIR /mysite

EXPOSE 3003

RUN adduser -D user

USER user

