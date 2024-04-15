FROM python:3.11

RUN pip install django celery

COPY ./requirements.txt /code/

WORKDIR / code

CMD python manage.py runserver 0.0.0.0:8000
