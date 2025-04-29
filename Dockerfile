FROM python:3.11-slim

# Install build tools for pandas / pyarrow wheels when necessary
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Default command (can be overridden with docker run ... <args>)
ENTRYPOINT ["python", "/app/main.py"]