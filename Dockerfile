FROM python:3.13-slim

LABEL maintainer="kruel1" \
      version="2.0" \
      description="CSV statistics CLI – summary, missing values, correlations, dtypes"

WORKDIR /app

# Install Python deps first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Default command (can be overridden with docker run ... <args>)
ENTRYPOINT ["python", "/app/main.py"]
