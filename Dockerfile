# Stage 1
FROM python:3.11-slim as base

ARG PYTHON_VER=3.11

WORKDIR /app

# Stage 2
FROM base as builder

COPY src/bot ./bot
COPY pyproject.toml pdm.lock ./
RUN pip install -U pip setuptools wheel
RUN pip install pdm
RUN mkdir __pypackages__ && pdm sync --prod --no-editable

# Stage 3
FROM base as runner

ENV PYTHONPATH=/app/pkgs

COPY --from=builder /app/__pypackages__/${PYTHON_VER}/lib ./pkgs
COPY --from=builder /app/__pypackages__/${PYTHON_VER}/bin/* ./bin/

CMD ["python", "-m", "bot"]
