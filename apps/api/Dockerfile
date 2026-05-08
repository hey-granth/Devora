FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY pyproject.toml ./
RUN pip install uv

# Install dependencies
RUN uv sync --dev

# Copy source code
COPY src/ ./src/
COPY alembic/ ./alembic/

# Expose port
EXPOSE 8000

# Default command
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
