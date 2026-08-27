FROM python:3.10-slim

WORKDIR /app

COPY src/ src/
COPY tests/ tests/

ENTRYPOINT ["python", "-m", "src.main"]
