FROM nginx:latest

# Create ssl directory
RUN mkdir -p /etc/nginx/ssl

# Copy script to create SSL
COPY ./docker/scripts/generate-ssl.sh /docker-entrypoint.d/

# Copy nginx configuration file
COPY ./docker/nginx/default.conf /etc/nginx/conf.d/default.conf

# Grant execution permission to the script
RUN chmod +x /docker-entrypoint.d/generate-ssl.sh 