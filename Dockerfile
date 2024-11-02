#pull official base image
FROM python:3.12.1-slim-bookworm

# configure poetry
ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache
ENV POETRY_VIRTUALENVS_CREATE=false


# install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# add poetry to path
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# set working directory
WORKDIR /src

# install dependencies
COPY pyproject.toml poetry.lock .
RUN poetry install

# run app
COPY . .
ENTRYPOINT ["/bin/bash", "-c", "poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]