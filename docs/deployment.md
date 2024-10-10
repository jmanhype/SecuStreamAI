# Deploying SecuStreamAI

This guide provides instructions for deploying SecuStreamAI in various environments.

## Prerequisites

- [Docker](https://www.docker.com/get-started) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 1.29.2 or higher)
- [Git](https://git-scm.com/downloads) (for cloning the repository)
- Access to a cloud provider (for cloud deployments)

## Environment Variables

Before deployment, ensure all environment variables are correctly set in the `.env` file. Key variables include:

- **Project Settings:**
  - `PROJECT_NAME`
  - `PROJECT_VERSION`
  - `API_V1_STR`

- **Kafka Configuration:**
  - `KAFKA_SERVER`
  - `KAFKA_TOPIC`

- **Redis Configuration:**
  - `REDIS_HOST`
  - `REDIS_PORT`

- **Prometheus Configuration:**
  - `PROMETHEUS_PORT`

- **Security Configuration:**
  - `OPENAI_API_KEY`
  - `SECRET_KEY`
  - `ALGORITHM`
  - `ACCESS_TOKEN_EXPIRE_MINUTES`

- **PostgreSQL Configuration:**
  - `POSTGRES_HOST`
  - `POSTGRES_PORT`
  - `POSTGRES_DB`
  - `POSTGRES_USER`
  - `POSTGRES_PASSWORD`

Ensure all environment variables are correctly set to allow seamless integration between services.

## Local Deployment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SecuStreamAI.git
   cd SecuStreamAI
   ```

2. Create a `.env` file by copying the example template:
   ```bash
   cp .env.example .env
   ```

3. Edit the `.env` file and configure your environment variables.

4. Build and start the Docker containers:
   ```bash
   docker-compose up --build -d
   ```

5. Apply database migrations:
   ```bash
   docker-compose exec app alembic upgrade head
   ```

6. Deploy the frontend:
   ```bash
   cd frontend
   docker build -t yourusername/secustreamai-frontend:latest .
   docker run -d -p 3000:3000 yourusername/secustreamai-frontend:latest
   ```

7. Access the application at http://localhost:8080

## Running Tests

Before deploying, it's recommended to run the test suite to verify that everything is functioning correctly:

```bash
docker-compose exec app pytest
```

## Cloud Deployment

### AWS

1. Set up an EC2 instance with Docker and Docker Compose installed.
2. Clone the repository on the EC2 instance.
3. Configure the `.env` file with production settings.
4. Build and start the Docker containers:
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```
5. Set up an Elastic Load Balancer to handle incoming traffic.
6. Configure security groups to allow necessary inbound traffic.

### Google Cloud Platform

1. Create a new VM instance in Google Compute Engine.
2. Install Docker and Docker Compose on the VM.
3. Clone the repository and configure the `.env` file.
4. Build and start the Docker containers:
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```
5. Set up a load balancer using Google Cloud Load Balancing.
6. Configure firewall rules to allow incoming traffic.

### GitHub Actions for Automated Deployments

To set up automated deployments using GitHub Actions, you need to configure the following secrets in your GitHub repository:

- `DOCKER_USERNAME`: Your Docker Hub username.
- `DOCKER_PASSWORD`: Your Docker Hub password.
- `SSH_PRIVATE_KEY`: Your SSH private key for accessing the deployment server.

To add these secrets:
1. Go to your repository on GitHub.
2. Click on `Settings` > `Secrets and variables` > `Actions`.
3. Click `New repository secret` and add the required secrets.

## Frontend Deployment

For cloud deployments, ensure the frontend is included in your `docker-compose.prod.yml`:

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  ports:
    - "3000:3000"
  environment:
    - REACT_APP_API_URL=${API_V1_STR}
  depends_on:
    - app
```

## Best Practices

- Use environment-specific docker-compose files (e.g., docker-compose.prod.yml).
- Implement proper logging and monitoring solutions.
- Regularly update and patch your systems.
- Use secrets management for sensitive information.
- Implement automated backups for your database.

## Scaling

To scale the application:

1. Increase the number of worker nodes in your cloud environment.
2. Adjust the replica count in your docker-compose file for scalable services.
3. Implement a distributed cache using Redis cluster.
4. Consider using managed Kafka and database services for better scalability.

## SSL Configuration

To set up SSL for secure communication:

1. Obtain SSL certificates for your domain (e.g., using Let's Encrypt).
2. Configure your web server (e.g., Nginx) to use the SSL certificates.
3. Update your docker-compose file to expose the secure port (usually 443).
4. Ensure all internal services communicate over secure channels.

## Monitoring

Use Prometheus and Grafana to monitor the application's performance and health:

1. Ensure Prometheus and Grafana containers are running (they should be included in your docker-compose file).
2. Access Prometheus at http://localhost:9090
   - Prometheus scrapes metrics from the FastAPI application, Kafka, Redis, and their respective exporters.
3. Access Grafana at http://your-domain:3000 (or the configured port).
4. Set up dashboards in Grafana to visualize key metrics from Prometheus.
5. Configure alerts for critical metrics to ensure timely response to issues.

## Troubleshooting

**Q1: How can I reset the database?**

A1: To reset the database, stop the Docker containers, remove the PostgreSQL volume, and start the services again:

```bash
docker-compose down
docker volume rm secustreamai_postgres_data
docker-compose up --build
```

**Q2: How do I update the application?**

A2: To update the application with the latest changes:

1. Pull the latest changes from the repository:
   ```bash
   git pull origin main
   ```
2. Rebuild and restart the Docker containers:
   ```bash
   docker-compose up --build -d
   ```
3. Apply any new database migrations:
   ```bash
   docker-compose exec app alembic upgrade head
   ```

Remember to always backup your data before performing major updates or resets.