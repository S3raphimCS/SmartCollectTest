FROM python:3.13-slim

ENV PROJECT_ROOT /project
ENV SRC_DIR /src
ENV DEPLOY_DIR ./deploy

RUN mkdir $PROJECT_ROOT
COPY $DEPLOY_DIR/gunicorn.conf.py $PROJECT_ROOT
COPY $DEPLOY_DIR/run_django.sh $PROJECT_ROOT

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev python3-dev && \
    apt-get clean

RUN pip install poetry

COPY ./$SRC_DIR/pyproject.toml $PROJECT_ROOT
COPY ./$SRC_DIR/poetry.lock $PROJECT_ROOT

WORKDIR $PROJECT_ROOT
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./$SRC_DIR $PROJECT_ROOT

RUN chmod +x $PROJECT_ROOT/run_django.sh
CMD ["/project/run_django.sh"]
