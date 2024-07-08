# FastAPI Application with Docker Compose

This repository contains a FastAPI application configured to run with Docker Compose. It includes services for FastAPI and PostgreSQL.

## Prerequisites

Make sure you have Docker and Docker Compose installed on your system.

- Docker installation instructions: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose installation instructions: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Setup

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <repository_name>

2. Build and Run:

    Build and start the services using Docker Compose

    docker-compose -f docker-compose.yml up -d --build

    This command builds the images if they do not exist and starts the services defined in docker-compose.yml.

3. Access the FastAPI app:

    Once Docker Compose has started the services, you can access the FastAPI application at:

    http://localhost:8000/swagger

4. Access the React Application

    http://localhost:3000

5. Connect to the postgres database using Dbeaver



 
