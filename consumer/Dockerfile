FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root

COPY . .

CMD ["python", "-m", "consumer.main"]
