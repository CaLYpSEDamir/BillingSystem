FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -U pip && pip install -r requirements.txt

COPY . /code

ENTRYPOINT ["/code/docker/docker-entrypoint.sh"]
