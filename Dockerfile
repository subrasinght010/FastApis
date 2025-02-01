# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable for Celery
ENV CELERY_BROKER_URL=redis://redis:6379/0

# Command to start the Celery worker
CMD ["celery", "-A", "app.tasks.app", "worker", "--loglevel=info"]
