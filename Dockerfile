# Use a lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy the sentinel script
COPY security_sentinel.py .

# Install dependencies
RUN pip install anthropic prometheus_client

# Expose the Prometheus metrics port
EXPOSE 8000

# Run the sentinel
CMD ["python", "security_sentinel.py"]
