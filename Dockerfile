FROM python:3.7.6

COPY requirements.txt /app/

WORKDIR /app/
RUN pip install -r requirements.txt

COPY docker_monitor /app/docker_monitor

