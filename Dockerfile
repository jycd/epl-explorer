FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    DATA_DIR=/app/data \
    PORT=5001

WORKDIR /app

# Install runtime deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (templates are inside src/)
COPY src ./src
COPY scripts ./scripts
COPY data ./data

EXPOSE ${PORT}

# Use the Flask dev server (not for production). Runs `src/app.py` which binds 0.0.0.0.
CMD ["python3", "src/app.py"]
