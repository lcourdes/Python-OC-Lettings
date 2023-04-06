FROM python:3.10-alpine

ADD . /app/
WORKDIR /app

ENV PORT=8000
ENV ALLOWED_HOSTS="localhost ec2-15-236-202-82.eu-west-3.compute.amazonaws.com 15.236.202.82"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE $PORT

CMD python manage.py makemigrations && python manage.py migrate && gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:$PORT