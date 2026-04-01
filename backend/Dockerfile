FROM python:3.11-slim
WORKDIR /app

RUN pip install uv

COPY pyproject.toml ./
RUN uv pip install --system ".[dev]"

COPY . .

ENV PYTHONPATH=/app
EXPOSE 8081

CMD ["uvicorn", "app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8081", "--reload"]
