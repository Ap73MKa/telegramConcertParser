# Stage 1
FROM python:3.11-alpine as builder

RUN pip install -U pip setuptools wheel
RUN pip install pdm

WORKDIR /app

COPY pyproject.toml pdm.lock ./
COPY src/ ./src

RUN mkdir __pypackages__ && pdm sync --prod --no-editable
ENV PYTHONPATH=/app/__pypackages__

CMD ["pdm", "run", "python", "-m", "src.bot"]
