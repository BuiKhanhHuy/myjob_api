.PHONY: setup-hosts generate-certs docker-up docker-down docker-build docker-restart docker-nginx-restart

# Setup hosts
setup-hosts:
	chmod +x ./docker/scripts/setup-hosts.sh
	sudo ./docker/scripts/setup-hosts.sh

# Start docker containers
docker-up:
	docker-compose up -d

# Stop docker containers
docker-down:
	docker-compose down

# Rebuild docker containers
docker-build:
	docker-compose build

# Restart nginx container
docker-nginx-restart:
	docker-compose restart nginx
# Setup everything (hosts + docker)
init: setup-hosts docker-build docker-up

# Show logs
logs:
	docker-compose logs -f
