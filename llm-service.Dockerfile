# Use the official Python base image
FROM python:3.12-slim

# Set the working directory inside the container
#WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY common /common
COPY llm_service /llm_service

# Expose the port on which the application will run
EXPOSE 8082

# Run the FastAPI application using uvicorn server
ENV PYTHONPATH=.
CMD uvicorn llm_service.llm_service:app --host 0.0.0.0 --port 8081
