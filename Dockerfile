FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
CMD ["./docker-entrypoint.sh"]