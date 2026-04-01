# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Start the application using Gunicorn, but run migrations first
CMD python manage.py migrate && exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 pilot_backend.wsgi:application
