FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN python manage.py collectstatic --noinput
CMD gunicorn hello_django.wsgi:application --bind 0.0.0.0:$PORT