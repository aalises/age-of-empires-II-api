FROM python:3.12.2-bookworm

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["gunicorn"  , "--bind", "0.0.0.0:8080", "app:app"]
