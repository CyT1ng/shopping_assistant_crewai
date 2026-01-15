FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
COPY README.md /app/README.md

RUN pip install -U pip && pip install -e .

ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "shop_assistant.main", "--query", "best budget mechanical keyboard under $80"]
