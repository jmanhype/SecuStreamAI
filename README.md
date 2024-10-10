# SecuStreamAI

![CI](https://github.com/yourusername/SecuStreamAI/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/yourusername/SecuStreamAI/actions/workflows/cd.yml/badge.svg)

![Docker Image](https://img.shields.io/docker/pulls/yourusername/secustreamai)
![License](https://img.shields.io/github/license/yourusername/SecuStreamAI)
![GitHub stars](https://img.shields.io/github/stars/yourusername/SecuStreamAI?style=social)

## Introduction

SecuStreamAI is a comprehensive security event processing system designed to generate, process, and analyze security events in real-time. Leveraging modern technologies such as Kafka, Redis, PostgreSQL, Prometheus, Grafana, and FastAPI, SecuStreamAI ensures scalability, reliability, and efficient data handling for security operations.

## Features

- **Real-time Event Processing**: Ingest and process security events using Kafka and Redis.
- **Adaptive Hybrid Analysis**: Combines rule-based, machine learning, and large language model approaches for comprehensive event analysis.
- **DSPy Integration**: Utilizes DSPy for configuring and fine-tuning language models for security analysis.
- **PyTorch Model**: Implements a neural network for quick event classification and risk assessment.
- **Scalable Architecture**: Easily scale components with Docker and Docker Compose.
- **Monitoring and Metrics**: Integrates Prometheus and Grafana for robust monitoring and visualization.
- **Secure Authentication**: Implements JWT-based authentication for secure access.
- **Automatic Database Migrations**: Manage database schema changes seamlessly with Alembic.
- **OpenAI Integration**: Utilize OpenAI's GPT models for advanced analytics and inference.
- **Continuous Learning**: Nightly fine-tuning of models to adapt to new security patterns.

## Adaptive Hybrid Approach

SecuStreamAI employs an innovative adaptive hybrid approach for security event analysis:

1. **Rule-Based Analysis**: Quick, deterministic rules for common security events.
2. **PyTorch Model**: A neural network for rapid event classification and initial risk assessment.
3. **DSPy-configured LLM**: Detailed analysis using a large language model for complex events.

The system dynamically chooses the most appropriate method based on event characteristics, balancing speed and depth of analysis. This approach ensures efficient resource utilization while providing comprehensive security insights.

### Continuous Improvement

- **Nightly Fine-tuning**: Both PyTorch and DSPy models are fine-tuned nightly to adapt to new security patterns.
- **Feedback Loop**: Analysis results are used to improve future predictions and update rule sets.

For more details on the architecture and components, please refer to the [Architecture Documentation](docs/architecture.md).

## Prerequisites

Before setting up SecuStreamAI, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 1.29.2 or higher)
- [Git](https://git-scm.com/downloads) (for cloning the repository)

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/SecuStreamAI.git
cd SecuStreamAI
```

### Environment Configuration

SecuStreamAI uses environment variables for configuration. Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit the `.env` file to set your environment variables:

```env
# Project Settings
PROJECT_NAME="SecuStreamAI"
PROJECT_VERSION="1.0.0"
API_V1_STR="/api/v1"

# Kafka Configuration
KAFKA_SERVER="kafka:29092"
KAFKA_TOPIC="security-events"

# Redis Configuration
REDIS_HOST="redis"
REDIS_PORT=6379

# Prometheus Configuration
PROMETHEUS_PORT=8000

# OpenAI Configuration
OPENAI_API_KEY="your_openai_api_key"

# Security Configuration
SECRET_KEY="your_secret_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# PostgreSQL Configuration
POSTGRES_HOST="postgres"
POSTGRES_PORT="5432"
POSTGRES_DB="secustreamai"
POSTGRES_USER="secustreamai_user"
POSTGRES_PASSWORD="your_secure_password"
```

**Note:** Replace placeholders like `your_openai_api_key`, `your_secret_key`, and `your_secure_password` with your actual credentials.

## Conda Environment Setup

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) if you haven't already.

2. Create the Conda environment using the provided `environment.yml` file:
   ```
   conda env create -f environment.yml
   ```

3. Activate the Conda environment:
   ```
   conda activate secustreamai
   ```

4. Verify the environment is set up correctly:
   ```
   python --version
   pip list
   ```

Make sure to activate this environment before running any scripts or starting the application.

## Running the Application

Use Docker Compose to build and run all the necessary services.

### Build and Start Services

```bash
docker-compose up --build
```

This command will build the Docker images (if not already built) and start all the services defined in the `docker/docker-compose.yaml` file, including:

- Zookeeper
- Kafka
- Redis
- PostgreSQL
- Prometheus
- Kafka Exporter
- Redis Exporter
- Grafana
- SecuStreamAI Application

### Run in Detached Mode (Optional)

To run the services in the background, use the `-d` flag:

```bash
docker-compose up --build -d
```

## Database Migrations

After starting the services, apply the database migrations to set up the necessary tables.

```bash
docker-compose exec app alembic upgrade head
```

This command runs Alembic migrations inside the `app` container, creating the `events` and `users` tables in the PostgreSQL database.

## Generating Security Events

To simulate and generate security events, use the provided event generator script.

1. **Run the Event Generator:**

   ```bash
   docker-compose exec app python scripts/generate_events.py
   ```

   This script will produce simulated security events to both Kafka and Redis at a configurable rate.

## Accessing the Services

Once all services are running, you can access them through the following URLs:

- **SecuStreamAI Application:**

  - **URL:** [http://localhost:8080](http://localhost:8080)

- **Prometheus:**

  - **URL:** [http://localhost:9090](http://localhost:9090)

- **Grafana:**

  - **URL:** [http://localhost:3000](http://localhost:3000)
  - **Default Credentials:**
    - **Username:** `admin`
    - **Password:** `admin` (Change this in the `.env` file for security)

## CI/CD Setup

To ensure seamless integration and deployment, set up GitHub Secrets and verify workflow executions.

### Set Up GitHub Secrets

For the workflows to function correctly, you need to set up the following secrets in your GitHub repository:

- `DOCKER_USERNAME`: Your Docker Hub username.
- `DOCKER_PASSWORD`: Your Docker Hub password.
- `SSH_PRIVATE_KEY`: Your SSH private key for accessing the deployment server.

**How to Add Secrets:**

1. Go to your repository on GitHub.
2. Click on `Settings` > `Secrets and variables` > `Actions`.
3. Click `New repository secret` and add the required secrets.

### Verify Workflow Execution

After setting up the workflows:

1. Push changes to the main branch or create a pull request.
2. Navigate to the `Actions` tab in your GitHub repository to monitor the workflow runs.
3. Ensure that all jobs (lint, test, build, and deploy) complete successfully.

## Monitoring and Metrics

SecuStreamAI integrates Prometheus and Grafana for monitoring and visualization.

1. **Prometheus:**

   - **URL:** [http://localhost:9090](http://localhost:9090)
   - **Configuration:** Prometheus scrapes metrics from the FastAPI application, Kafka, Redis, and their respective exporters.

2. **Grafana:**

   - **URL:** [http://localhost:3000](http://localhost:3000)
   - **Setup Dashboards:**
     - After logging in, add Prometheus as a data source.
     - Import or create dashboards to visualize metrics such as event counts, processing times, and system health.

## Screenshots

![Dashboard Screenshot](docs/screenshots/dashboard.png)

## Usage Examples

### Fetching Security Events

```bash
curl -X GET "http://localhost:8080/api/v1/events" -H "accept: application/json"
```

### Creating a New User

```bash
curl -X POST "http://localhost:8080/api/v1/users" -H "accept: application/json" -H "Content-Type: application/json" -d '{"username":"john_doe","password":"securepassword"}'
```

## Testing

Before deploying, it's recommended to run the test suite to verify that everything is functioning correctly.

### Running Tests

```bash
docker-compose exec app pytest
```

## Deployment

For deploying SecuStreamAI to a production environment, consider the following steps:

1. **Set Up a Production Server:**
   - Ensure the server has Docker and Docker Compose installed.

2. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/SecuStreamAI.git
   cd SecuStreamAI
   ```

3. **Configure Environment Variables:**
   - Update the `.env` file with production-specific settings.

4. **Build and Deploy:**

   ```bash
   docker-compose up --build -d
   ```

5. **Apply Migrations:**

   ```bash
   docker-compose exec app alembic upgrade head
   ```

6. **Set Up SSL:**
   - Configure SSL certificates for secure communication.

7. **Monitor Services:**
   - Use Prometheus and Grafana to monitor the application's performance and health.

## Frequently Asked Questions (FAQ)

**Q1: How can I reset the database?**

A1: To reset the database, stop the Docker containers, remove the PostgreSQL volume, and start the services again.

```bash
docker-compose down -v
docker-compose up --build
```

**Q2: How do I change the event generation rate?**

A2: Modify the `events_per_second` parameter in the `generate_events.py` script or adjust the sleep interval as needed.

## Stopping the Application

To stop all running services, execute:

```bash
docker-compose down
```

This command stops and removes all containers defined in the `docker/docker-compose.yaml` file.

## Troubleshooting

- **Alembic Import Errors:**
  - Ensure all environment variables are correctly set in the `.env` file.
  - Verify that the `app` service is running before applying migrations.

- **Service Connectivity Issues:**
  - Check if all services are up and running using:

    ```bash
    docker-compose ps
    ```

  - Review logs for any errors:

    ```bash
    docker-compose logs [service_name]
    ```

- **Port Conflicts:**
  - Ensure that the ports defined in the `docker-compose.yaml` are not occupied by other applications.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes with clear messages.
4. Push your branch and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or feedback, please contact [your.email@example.com](mailto:your.email@example.com).

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Docker](https://www.docker.com/)
- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Confluent Kafka](https://www.confluent.io/)