# SecuStreamAI Architecture

## Overview

SecuStreamAI is a comprehensive security event processing system designed to generate, process, and analyze security events in real-time. The architecture leverages various technologies such as Kafka, Redis, PostgreSQL, Prometheus, Grafana, and FastAPI to ensure scalability, reliability, and efficient data handling.

## Architecture Diagram

> **Figure:** High-level architecture diagram of SecuStreamAI.
>
> ![Architecture Diagram](docs/architecture_diagram.png)
>


## Components

### 1. User Interface

- **Web Dashboard**
  - **Description:** Provides a user-friendly interface for monitoring and managing security events and analytics.
  - **Technologies:** FastAPI, Uvicorn, Grafana (for visualization).

- **Authentication Service**
  - **Description:** Handles user authentication and authorization to secure access to the dashboard and APIs.
  - **Technologies:** FastAPI, JWT (JSON Web Tokens).

### 2. Event Generation and Processing

- **Event Generator**
  - **Description:** Simulates and generates security events to populate the system for processing and analysis.
  - **Technologies:** Python, Kafka Producer, Redis.

- **Adaptive Hybrid Analyzer**
  - **Description:** Core component that decides and applies the most appropriate analysis method for each security event.
  - **Technologies:** Python, PyTorch, DSPy, OpenAI GPT.

### 3. Message Brokers

- **Kafka**
  - **Description:** Acts as a high-throughput distributed messaging system for handling event streams.
  - **Technologies:** Apache Kafka, Zookeeper.

- **Redis**
  - **Description:** Serves as an in-memory data store for caching and quick data retrieval.
  - **Technologies:** Redis Server, Redis Exporter.

### 4. Database

- **PostgreSQL**
  - **Description:** Relational database for storing structured data such as user information and event details.
  - **Technologies:** PostgreSQL 13, SQLAlchemy, Alembic for migrations.

### 5. Analytics and Monitoring

- **Prometheus**
  - **Description:** Monitoring and alerting toolkit for collecting metrics from various services.
  - **Technologies:** Prometheus Server, Prometheus Config.

- **Grafana**
  - **Description:** Visualization tool for displaying metrics and analytics data collected by Prometheus.
  - **Technologies:** Grafana, Grafana Dashboards and Provisioning.

### 6. Application Backend

- **FastAPI Application**
  - **Description:** Core backend application handling API requests, event processing, and interfacing with other services.
  - **Technologies:** FastAPI, Uvicorn, SQLAlchemy, Alembic, Pydantic, Python.

### 7. Machine Learning Components

- **Rule-Based Analyzer**
  - **Description:** Implements quick, deterministic rules for common security events.
  - **Technologies:** Python.

- **PyTorch Model**
  - **Description:** Neural network for rapid event classification and initial risk assessment.
  - **Technologies:** PyTorch, BERT.

- **DSPy-configured LLM**
  - **Description:** Large Language Model configured with DSPy for detailed analysis of complex events.
  - **Technologies:** DSPy, OpenAI GPT.

### 8. Exporters

- **Kafka Exporter**
  - **Description:** Exposes Kafka metrics to Prometheus for monitoring.
  - **Technologies:** `danielqsj/kafka-exporter`.

- **Redis Exporter**
  - **Description:** Exposes Redis metrics to Prometheus for monitoring.
  - **Technologies:** `oliver006/redis_exporter`.

## Adaptive Hybrid Approach

SecuStreamAI employs an innovative adaptive hybrid approach for security event analysis:

1. **Event Ingestion:** Security events are ingested through Kafka and temporarily stored in Redis for quick access.

2. **Analysis Method Selection:** The Adaptive Hybrid Analyzer determines the most appropriate analysis method based on event characteristics:
   - Common, low-risk events are processed by the Rule-Based Analyzer.
   - Events requiring quick classification are sent to the PyTorch Model.
   - Complex events needing detailed analysis are processed by the DSPy-configured LLM.

3. **Analysis Execution:** The selected method processes the event, generating risk assessments, recommended actions, and detailed analyses.

4. **Result Storage and Distribution:** Analysis results are stored in PostgreSQL and distributed to relevant components for visualization and further processing.

5. **Continuous Learning:** 
   - The PyTorch Model and DSPy-configured LLM undergo nightly fine-tuning to adapt to new security patterns.
   - A feedback loop incorporates analysis results to improve future predictions and update rule sets.

This approach ensures efficient resource utilization while providing comprehensive security insights, balancing between speed and depth of analysis based on each event's characteristics.

## Workflow

1. **Event Generation:**
   - The **Event Generator** creates simulated security events.
   - Events are sent to **Kafka** and **Redis** for distribution and quick access.

2. **Message Brokering:**
   - **Kafka** handles the high-throughput event streams, ensuring reliable delivery to various consumers.
   - **Redis** provides fast in-memory access for caching frequently accessed data.

3. **Data Storage:**
   - Critical event data and user information are stored in **PostgreSQL**.
   - **Alembic** manages database schema migrations, ensuring the database remains in sync with the application models.

4. **Application Backend:**
   - The **FastAPI** application exposes RESTful APIs for interacting with events and analytics.
   - It processes incoming events, performs necessary computations, and updates the database accordingly.

5. **Analytics and Monitoring:**
   - **Prometheus** scrapes metrics from all services, including Kafka, Redis, PostgreSQL, and the FastAPI application.
   - **Grafana** visualizes these metrics, providing insights into system performance and security event trends.

6. **Visualization and Dashboard:**
   - Users interact with the **Web Dashboard** to monitor security events, view analytics, and manage system configurations.
   - **Grafana** dashboards are integrated into the web interface for comprehensive data visualization.

## Environment Configuration

Configuration is managed through environment variables defined in the `.env` file located at the project root. Key configurations include:

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

Ensure all environment variables are correctly set in the `.env` file to allow seamless integration between services.

## Deployment

Deployment is managed using Docker and Docker Compose. The `docker/docker-compose.yaml` file defines all necessary services, their configurations, and dependencies. To deploy the application:

1. **Build and Start Services:**

   ```bash
   docker-compose up --build
   ```

2. **Apply Database Migrations:**

   ```bash
   docker-compose exec app alembic upgrade head
   ```

3. **Access Services:**
   - **Web Dashboard:** `http://localhost:8080`
   - **Prometheus:** `http://localhost:9090`
   - **Grafana:** `http://localhost:3000` (Default credentials: `admin/admin`)

## Scalability and Performance

- **Kafka** ensures high-throughput event streaming, handling large volumes of security events efficiently.
- **Redis** provides low-latency data access, crucial for real-time analytics and caching.
- **PostgreSQL** scales vertically and horizontally to handle growing data storage needs.
- **Prometheus** and **Grafana** offer robust monitoring capabilities, allowing for proactive scaling and optimization based on system metrics.

## Security Considerations

- **Authentication:** Implemented via JWT in the Authentication Service to secure API endpoints.
- **Environment Variables:** Sensitive information is managed through environment variables and not hard-coded.
- **Data Integrity:** Referential integrity is enforced between `User` and `Event` tables using foreign key constraints.

## Conclusion

SecuStreamAI's architecture is designed to provide a robust, scalable, and efficient platform for security event processing and analysis. By leveraging industry-standard technologies and best practices, the system ensures high performance, reliability, and security.
