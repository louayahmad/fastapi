# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install additional utilities
RUN apt-get update && apt-get install -y wget

# Download wait-for-it.sh
RUN wget -O /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /usr/local/bin/wait-for-it.sh

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Command to run the application, waiting for PostgreSQL to be ready
CMD ["wait-for-it.sh", "postgres_db:5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
