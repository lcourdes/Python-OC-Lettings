FROM python:3.10-alpine

ADD . /app/
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py makemigrations && python manage.py migrate && gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:8000