FROM python:3.12-bullseye

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app/ ./app

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.wsgi:g_app", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "debug"]

# CMD ["flask", "--app", "app", "run"]