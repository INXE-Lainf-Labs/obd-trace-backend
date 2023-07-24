FROM python:3.11.3-bullseye as builder
WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y libmagic-dev
COPY . /usr/src/app
RUN ls -la
RUN python -m pip install -U pip && pip install -r src/config/requirements.txt

FROM builder as dev
RUN pip install -r src/config/requirements/dev.txt
ENTRYPOINT ["sh", "docker/api-entrypoint-scripts/docker-entrypoint.sh"]

FROM builder as prod
ENTRYPOINT ["sh", "docker/api-entrypoint-scripts/docker-entrypoint.sh"]
