FROM python:3.10-alpine
WORKDIR /app/backend

RUN apk update && apk add python3-dev gcc libc-dev
RUN python -m pip install --upgrade pip

COPY ./backend/requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY ./backend .
RUN python manage.py migrate
RUN python manage.py collectstatic

ENV DJANGO_SUPERUSER_PASSWORD "99999999"
RUN python manage.py createsuperuser --username gu999999 --email admin@example.com --noinput