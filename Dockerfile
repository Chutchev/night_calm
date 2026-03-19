# Use a lightweight Python base image
# This specific tag supports multiple architectures, including linux/amd64 and linux/arm64
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Set environment variables
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install system dependencies if any are needed
# For a basic aiogram bot, slim-python usually has all we need,
# but we might need build-essential if some wheels aren't pre-built for ARM64.
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to take advantage of Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure .env is not baked into the image (handled by .dockerignore)
# But remind the user to provide it at runtime

# Command to run the bot
CMD ["python", "main.py"]
