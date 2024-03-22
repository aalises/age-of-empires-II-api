FROM python:latest

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["gunicorn","--config", "gunicorn_config.py", "app:app"]
