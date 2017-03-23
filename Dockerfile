FROM python:latest
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app

ENTRYPOINT ["/app/docker_entrypoint.sh"]
