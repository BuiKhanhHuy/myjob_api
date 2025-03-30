# Use the official Python image
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential libssl-dev libffi-dev \
        libopenblas-dev default-libmysqlclient-dev \
        pkg-config curl netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /myjob_api

# Copy the requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code into the container
COPY . .

COPY docker/scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]