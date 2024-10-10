# SecuStreamAI Usage Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Environment Configuration](#environment-configuration)
4. [Setting Up the Project](#setting-up-the-project)
5. [Running the Application](#running-the-application)
6. [Database Migrations](#database-migrations)
7. [Generating Security Events](#generating-security-events)
8. [Accessing the Services](#accessing-the-services)
9. [Monitoring and Metrics](#monitoring-and-metrics)
10. [Stopping the Application](#stopping-the-application)
11. [Troubleshooting](#troubleshooting)
12. [Additional Resources](#additional-resources)

---

## Introduction

SecuStreamAI is a comprehensive security event processing system designed to generate, process, and analyze security events in real-time. This guide provides step-by-step instructions to set up, run, and interact with SecuStreamAI using Docker Compose.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- [Docker](https://www.docker.com/get-started) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 1.29.2 or higher)
- [Git](https://git-scm.com/downloads) (for cloning the repository)

## Environment Configuration

SecuStreamAI uses environment variables to manage configurations. These variables are defined in a `.env` file located at the root of the project.

### Creating the `.env` File

1. Navigate to the root directory of your project:
   
   ```bash
   cd /path/to/SecuStreamAI
   ```
   
2. Create a `.env` file by copying the example template:

   ```bash
   cp .env.example .env
   ```

3. Open the `.env` file in your preferred text editor and set the necessary environment variables:

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

## Setting Up the Project

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/SecuStreamAI.git
   cd SecuStreamAI
   ```

2. **Ensure Docker is Running:**

   Make sure Docker and Docker Compose are installed and running on your system.

## Running the Application

Use Docker Compose to build and run all the necessary services.

1. **Build and Start Services:**

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

2. **Run in Detached Mode (Optional):**

   To run the services in the background, use the `-d` flag:

   ```bash
   docker-compose up --build -d
   ```

## Database Migrations

After starting the services, apply the database migrations to set up the necessary tables.

1. **Apply Migrations:**

   ```bash
   docker-compose exec app alembic upgrade head
   ```

   This command runs Alembic migrations inside the `app` container, creating the `events` and `users` tables in the PostgreSQL database.

## Generating Security Events

To simulate and generate security events, use the provided event generator script.

1. **Run the Event Generator:**

   Open a new terminal window and navigate to the project directory, then execute:

   ```bash
   docker-compose exec app python scripts/generate_events.py
   ```

   This script will produce simulated security events to both Kafka and Redis at a configurable rate.

## Interacting with the Adaptive Hybrid Analyzer

The Adaptive Hybrid Analyzer is a core component of SecuStreamAI. Here's how to interact with it:

1. **Sending Events for Analysis:**

   Use the FastAPI endpoint to send security events for analysis:

   ```bash
   curl -X POST "http://localhost:8080/api/v1/events/analyze" \
        -H "Content-Type: application/json" \
        -d '{"context": "login attempt", "event_description": "Failed login from IP 192.168.1.100"}'
   ```

2. **Viewing Analysis Results:**

   Retrieve analysis results using the event ID returned from the analyze endpoint:

   ```bash
   curl "http://localhost:8080/api/v1/events/{event_id}"
   ```

3. **Monitoring Analysis Methods:**

   Check which analysis method was used for recent events:

   ```bash
   curl "http://localhost:8080/api/v1/events/analysis_methods"
   ```

4. **Triggering Model Fine-tuning:**

   To manually trigger the nightly fine-tuning process:

   ```bash
   docker-compose exec app python scripts/finetune_models.py
   ```

5. **Updating Rule-Based Analyzer:**

   To update rules in the Rule-Based Analyzer, edit the `src/analyzers/rule_based_analyzer.py` file and restart the application:

   ```bash
   docker-compose restart app
   ```

These interactions allow you to fully utilize the adaptive hybrid approach of SecuStreamAI.

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
   - **Adaptive Hybrid Analyzer Dashboard:**
     - Import the pre-configured dashboard for monitoring the adaptive hybrid approach.
     - This dashboard shows metrics such as:
       - Distribution of analysis methods used
       - Processing time for each analysis method
       - Model accuracy and confidence scores
       - Rule-based analyzer hit rates

## Stopping the Application

To stop all running services, execute:

```
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