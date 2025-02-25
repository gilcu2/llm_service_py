# Use the official Python base image
FROM python:3.12-slim

# Set the working directory inside the container
#WORKDIR /app

#
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY common /common
COPY history_service /history_service

# Expose the port on which the application will run
EXPOSE 8083

# Run the FastAPI application using uvicorn server
ENV PYTHONPATH=.
CMD uvicorn history_service.history_service:app --host 0.0.0.0 --port 8083