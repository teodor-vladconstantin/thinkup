# ThinkUp Platform

Central monorepo for the **ThinkUp Academy** platform, containing the frontend, backend, and infrastructure configuration required to run the full stack locally or in production.

## Project Structure

- **`platform-frontend/`** — Web application built with **Next.js**.
- **`platform-backend/`** — API built with **Python Flask**, including database scripts.
- **`platform-backend/docker-compose.yml`** — Main configuration for running the full stack locally (frontend, backend, database, and reverse proxy).

## Documentation

- **[ONBOARDING.md](ONBOARDING.md)** — Guide for new developers (local setup and installation).
- **[DEPLOY_VPS.md](DEPLOY_VPS.md)** — Guide for deploying to a production VPS.

## Tech Stack

- **Frontend:** Next.js
- **Backend:** Python (Flask)
- **Database:** ScyllaDB
- **Infrastructure:** Docker, Nginx
- **Authentication:** Auth0

## Running the Project (Docker)

The simplest way to run the application is with Docker Compose.

### 1. Prerequisites

Make sure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is installed and running.

### 2. Environment Variables (Frontend)

Before starting the stack, the frontend needs Auth0 credentials.

1. Go to the `platform-frontend` folder.
2. Create a file named `.env.local` (copy the example from `.env.example`).
3. Fill in the required variables:

```bash
# platform-frontend/.env.local

AUTH0_SECRET='...'           # Generate with `openssl rand -hex 32`
AUTH0_BASE_URL='http://localhost:3000'
AUTH0_ISSUER_BASE_URL='...'  # Your Auth0 domain
AUTH0_CLIENT_ID='...'        # Client ID from Auth0
AUTH0_CLIENT_SECRET='...'    # Client Secret from Auth0
NEXT_PUBLIC_API_URL='http://localhost' # API URL (via Nginx/Docker)
```

### 3. Start the Platform

Open a terminal and run:

```bash
# Go to the backend folder, where the Docker configuration lives
cd platform-backend

# Start all containers (Frontend + Backend + ScyllaDB + Nginx)
docker-compose up --build -d
```

### 4. Access

Once the containers are up (the first run may take a few minutes while ScyllaDB initializes):

- **Frontend:** [http://localhost:3000](http://localhost:3000)
- **API:** the `backend` container does not publish a host port in `docker-compose.yml`; it is only reachable through the `nginx` container.

> **Note:** `platform-backend/nginx/conf.d/default.conf` is currently configured for the production domain (`thinkupacademy.ro`) and requires Let's Encrypt certificates to start. Running `docker-compose up` locally as-is will likely fail to bring up `nginx` without those certificates. If you need direct local access to the API, use `docker exec` into the `backend` container, or adjust the Nginx config for local development.

## Useful Commands

**Stop the stack:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f
```

**Manual database initialization (if needed):**
If the database is not populated automatically, run the initialization script from `platform-backend`:
```bash
python init_local_db.py
```
