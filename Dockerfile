# Stage 1
FROM python:3.11-slim as base

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Stage 2
FROM base as builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_VERSION=1.5.1

COPY pyproject.toml poetry.lock ./
RUN pip install -U pip setuptools
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry install --without dev --no-root

# Stage 3
FROM base as runner

ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app/.venv ./.venv
COPY ./bot ./bot
CMD ["python", "-m", "bot"]
