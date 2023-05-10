# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set environment variable for runtime detection
ENV DOCKER_CONTAINER=1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app

# Copy requirements.txt separately to avoid rebuilding the image
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run main.py when the container launches
CMD ["python", "main.py"]
