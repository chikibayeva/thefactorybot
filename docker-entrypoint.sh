#!/bin/sh

container_type=${CONTAINER_TYPE-BACKEND};

cd src

if [ $container_type = "CELERY" ]; then
    celery -A app.celery worker --queues=thefactorybot-celery --loglevel=INFO --concurrency=2
elif [ $container_type = "APPLICATION" ]; then
    ls
    python manage.py collectstatic --noinput --clear
    python manage.py migrate --noinput
    python manage.py runserver 0.0.0.0:8000
fi;
