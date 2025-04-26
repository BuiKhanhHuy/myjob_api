# Use the official Python image
FROM python:3.10-slim

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

CMD ["sh", "-c", "sleep 30 && python manage.py runserver 0.0.0.0:8000"]

EXPOSE 8000