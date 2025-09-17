FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    kubectl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test files
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTEST_CURRENT_TEST=true

# Default command
CMD ["pytest", "-v", "--tb=short"]
