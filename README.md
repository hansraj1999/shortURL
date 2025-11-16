# shortURL

shortURL is a URL shortening service that utilizes Redis, MongoDB, and Python's Squid library for efficient and distributed URL hashing and storage. The application also includes NGINX for request distribution and provides monitoring capabilities with Prometheus and Grafana.

## Features
- **Redis**: Uses the `INCR` method to generate unique IDs.
- **MongoDB**: Stores the mapping of shortened URLs to original URLs.
- **Distributed Locking**: Ensures thread-safe operations.
- **NGINX**: Distributes incoming requests for load balancing.
- **Prometheus and Grafana**: Monitors application metrics and health checks.
- **Health Checks**: Includes health check endpoints for monitoring container status.
- **Analytics**: Track redirect counts, view total URLs shortened, and filter/sort analytics data by various criteria.

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

### Get Analytics
Use the following `curl` commands to retrieve analytics data for shortened URLs:

#### Basic Analytics (Default: sorted by creation date, descending)
```bash
curl -X 'GET' \
  'http://localhost/v1/analytics' \
  -H 'accept: application/json' \
  -H 'headers: {   "x-user-data": {  "role":"company",   "user_name": "hansraj",     "user_id": 1   },   "role": "company" }'
```

#### Sort by Redirect Count (Most Popular First)
```bash
curl -X 'GET' \
  'http://localhost/v1/analytics?sort_by=hits&sort_order=desc' \
  -H 'accept: application/json' \
  -H 'headers: {   "x-user-data": {  "role":"company",   "user_name": "hansraj",     "user_id": 1   },   "role": "company" }'
```

#### Sort by Latest Shortened URLs
```bash
curl -X 'GET' \
  'http://localhost/v1/analytics?sort_by=latest_shortened&sort_order=desc' \
  -H 'accept: application/json' \
  -H 'headers: {   "x-user-data": {  "role":"company",   "user_name": "hansraj",     "user_id": 1   },   "role": "company" }'
```

#### Sort by Latest Redirected URLs
```bash
curl -X 'GET' \
  'http://localhost/v1/analytics?sort_by=latest_redirected&sort_order=desc' \
  -H 'accept: application/json' \
  -H 'headers: {   "x-user-data": {  "role":"company",   "user_name": "hansraj",     "user_id": 1   },   "role": "company" }'
```

#### Filter by User ID
```bash
curl -X 'GET' \
  'http://localhost/v1/analytics?filter_by_user_id=1&sort_by=hits&sort_order=desc' \
  -H 'accept: application/json' \
  -H 'headers: {   "x-user-data": {  "role":"company",   "user_name": "hansraj",     "user_id": 1   },   "role": "company" }'
```

#### Filter by User Name
```bash
curl -X 'GET' \
  'http://localhost/v1/analytics?filter_by_user_name=hansraj&sort_by=latest_redirected&sort_order=desc' \
  -H 'accept: application/json' \
  -H 'headers: {   "x-user-data": {  "role":"company",   "user_name": "hansraj",     "user_id": 1   },   "role": "company" }'
```

#### Pagination (Limit and Skip)
```bash
curl -X 'GET' \
  'http://localhost/v1/analytics?limit=50&skip=0&sort_by=hits&sort_order=desc' \
  -H 'accept: application/json' \
  -H 'headers: {   "x-user-data": {  "role":"company",   "user_name": "hansraj",     "user_id": 1   },   "role": "company" }'
```

#### Analytics Query Parameters
- `sort_by`: Sort field - Options: `hits`, `redirect_count`, `created_at`, `latest_shortened`, `last_redirected_at`, `latest_redirected` (default: `created_at`)
- `sort_order`: Sort direction - Options: `asc`, `desc` (default: `desc`)
- `filter_by_user_id`: Filter results by user ID (optional)
- `filter_by_user_name`: Filter results by user name (optional)
- `limit`: Number of results to return (default: 100, max: 1000)
- `skip`: Number of results to skip for pagination (default: 0)

## Database Schema and Indexes

For detailed information about the database schema and indexes, see [Database Schema Documentation](docs/DATABASE_SCHEMA.md).

The application automatically creates optimized indexes for:
- Fast URL lookups by hash
- Efficient filtering by user (user_id, user_name)
- Optimized sorting by redirect count, creation date, and last redirect time
- Compound indexes for common query patterns (user + sort combinations)

To manually create indexes, run:
```bash
python migerations/create_indexes.py
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