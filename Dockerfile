# Use specific version for stability
FROM python:3.11-slim

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy configuration files
COPY pyproject.toml .

# Install dependencies (including the project itself in editable mode for dev)
# Note: We copy the rest of the code later to use Docker cache effectively
COPY src/ src/
COPY main.py .
RUN pip install -e .

# Create non-root user
RUN useradd -m -s /bin/bash appuser && chown -R appuser /app
USER appuser

# Expose Streamlit port
EXPOSE 8501

# Default command
CMD ["python", "main.py", "--help"]