# shortURL

shortURL is a URL shortening service that utilizes Redis, MongoDB, and Python's Squid library for efficient and distributed URL hashing and storage. The application also includes NGINX for request distribution and provides monitoring capabilities with Prometheus and Grafana.

## Features
- **Redis**: Uses the `INCR` method to generate unique IDs.
- **MongoDB**: Stores the mapping of shortened URLs to original URLs.
- **Distributed Locking**: Ensures thread-safe operations.
- **NGINX**: Distributes incoming requests for load balancing.
- **Prometheus and Grafana**: Monitors application metrics and health checks.
- **Health Checks**: Includes health check endpoints for monitoring container status.

## Accessing Monitoring Tools
Integrated Prometheus and Grafana to help monitor the service.

### Prometheus
- Visit the Prometheus dashboard to monitor targets:
  - **URL**: [http://localhost:9090/targets](http://localhost:9090/targets)

### Grafana
- Access the Grafana dashboard to visualize metrics:
  - **URL**: [http://localhost:3000/](http://localhost:3000/)
  - **Username**: `admin`
  - **Password**: `admin`

## Usage

### Create a Short URL
Use the following `curl` command to create a shortened URL:
```bash
curl -X 'POST' \
  'http://localhost/v1/shorten' \
  -H 'accept: application/json' \
  -H 'headers: {   "x-user-data": {  "role":"company",   "user_name": "hansraj",     "user_id": 1   },   "role": "company" }' \
  -H 'Content-Type: application/json' \
  -d '{
  "long_url": "https://www.netflix.com/",
  "group_guid": "string",
  "qr_code": true,
  "custom_domain": "string"
}'
```

### Redirect to Original URL
Use the following `curl` command to redirect from the shortened URL to the original URL:

```bash
curl -X 'GET' \
  'http://localhost/gb' \
  -H 'accept: application/json'
```

## Running Locally

### Quick Start
To set up and run the application locally, you can use the provided setup script or run Docker Compose commands manually.

#### Using Setup Script
```bash
./local_setup/local_setup.sh --mode app
./local_setup/local_setup.sh --mode full
./local_setup/local_setup.sh --rebuild
```

#### If in hurry or facing any issue can run these:
```bash
docker network create bithash > /dev/null
docker compose -f ./docker_compose_full.yml up --scale app=3
```