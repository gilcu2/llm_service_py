# Use the official Python base image
FROM python:3.12-slim

# Set the working directory inside the container
#WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
RUN  ollama pull llama3.2

# Expose the port on which the application will run
EXPOSE 11434

CMD ollama serve
