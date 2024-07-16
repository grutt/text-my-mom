# Use the official Python image as a base image
FROM python:3.10-slim

# Set environment variables
ENV POETRY_VERSION=1.4.2

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the working directory
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application code to the working directory
COPY src /app/src

# Set the entrypoint to run the start script
ENTRYPOINT ["poetry", "run", "start"]
