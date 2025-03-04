# Use the official Python image
FROM python:3.10-slim

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential libssl-dev libffi-dev \
        libopenblas-dev default-libmysqlclient-dev \
        pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /myjob_api

# Copy the requirements file and install Python packages
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy the code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000