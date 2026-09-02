FROM python:3.11-slim

# Force Python stdout & stderr streams to be unbuffered for instant Cloud Logging
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Install system build dependencies for C-extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and pre-indexed data stores
COPY . .

EXPOSE 8080

# Execute uvicorn as PID 1 directly with shell expansion
CMD exec uvicorn app:app --host 0.0.0.0 --port $PORT
