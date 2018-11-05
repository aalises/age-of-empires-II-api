FROM tiangolo/uwsgi-nginx-flask:python3.7
COPY . /app
RUN pip install -r requirements.txt



