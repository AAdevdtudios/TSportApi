FROM python:3.11.0-slim-buster

WORKDIR /BACKEND

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "gunicorn", "core.wsgi" ]

# CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000", "--noreload" ]