#!/bin/bash

# Create ssl directory
mkdir -p ./nginx/ssl

# Check and install mkcert if not exists
if ! command -v mkcert &> /dev/null; then
    echo "Installing mkcert..."
    brew install mkcert
    mkcert -install
fi

# Generate SSL certificate
mkcert -key-file ./nginx/ssl/private.key -cert-file ./nginx/ssl/certificate.crt localhost 127.0.0.1

# Set permissions
chmod 644 ./nginx/ssl/private.key
chmod 644 ./nginx/ssl/certificate.crt

echo "SSL certificates generated successfully!"

# Start docker compose
docker compose down
docker compose up -d

echo "Application started with HTTPS enabled!" 