#!/bin/sh

# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/private.key \
  -out /etc/nginx/ssl/certificate.crt \
  -subj "/C=VN/ST=HCM/L=HCM/O=Local Development/OU=IT/CN=localhost"

# Set permissions for files
chmod 644 /etc/nginx/ssl/private.key
chmod 644 /etc/nginx/ssl/certificate.crt

echo "SSL certificates generated successfully!"