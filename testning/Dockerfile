FROM ubuntu:22.04

# Set working directory
WORKDIR /app

# Install system dependencies including Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps

# Copy test files
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTEST_CURRENT_TEST=true

# Default command
CMD ["python3", "-m", "pytest", "-v", "--tb=short"]
