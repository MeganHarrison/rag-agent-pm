FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared utilities
COPY ../../shared /app/shared

# Copy service code
COPY src/ /app/src/

# Set Python path
ENV PYTHONPATH=/app

EXPOSE 8002

# Copy startup script
COPY start.py .

# Ensure start.py is executable and set explicit entrypoint
RUN chmod +x start.py

CMD ["python", "-u", "start.py"]