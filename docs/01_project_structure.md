# Project Structure and Infrastructure

This document provides an overview of the project structure, Docker setup, and development environment.

## High-Level Architecture

The project is an "Agentic Operational Intelligence System" designed to analyze operational data from a version control system (like Git) and a project management tool (like Jira) and present it through a web dashboard. It consists of two main services orchestrated by Docker Compose:

1.  **`analyzer`**: A batch job that runs a `crewai`-based agentic crew to perform data analysis.
2.  **`dashboard`**: A Streamlit web application that visualizes the results from the `analyzer`.

These services communicate via **AWS S3** (or a local equivalent like LocalStack). The `analyzer` uploads its results to an S3 bucket, and the `dashboard` reads from it.

## Directory Structure

```
ops-intelligence/
├── .devcontainer/
│   └── devcontainer.json   # VS Code Dev Container configuration
├── .env.example            # Example environment variables
├── .gitignore
├── docker-compose.yml      # Docker Compose for service orchestration
├── Dockerfile              # Docker image definition for the services
├── init-aws.sh             # Script to initialize LocalStack resources
├── main.py                 # Entry point for the application (CLI)
├── pyproject.toml          # Python project metadata and dependencies
├── README.md
├── docs/                   # Project documentation
└── src/
    ├── ops_intelligence/   # Source code for the 'analyzer' service
    │   ├── config/
    │   │   ├── agents.yaml # Agent definitions
    │   │   └── tasks.yaml  # Task definitions
    │   ├── tools/          # Custom tools for agents
    │   └── crew.py         # Crew definition and task orchestration
    └── web/
        └── dashboard.py    # Source code for the Streamlit 'dashboard'
```

## Infrastructure Setup

### Docker

The entire application is containerized, and the setup is defined in `Dockerfile` and `docker-compose.yml`.

#### `Dockerfile`

The `Dockerfile` defines the common image for both the `analyzer` and `dashboard` services. It starts from a Python 3.11 base image, installs the dependencies from `pyproject.toml` (via Poetry), and sets up the working directory.

#### `docker-compose.yml`

The `docker-compose.yml` file orchestrates the multi-service application:

-   **`analyzer` service**:
    -   Builds from the `Dockerfile`.
    -   Runs the command `python main.py analyze` to start the analysis process.
    -   Connects to the `localstack` service for AWS emulation.
    -   Mounts the `src` directory into the container.

-   **`dashboard` service**:
    -   Also builds from the same `Dockerfile`.
    -   Runs the command `python main.py dashboard` to start the web server.
    -   Exposes port `8501` for the Streamlit dashboard.
    -   Connects to the `localstack` service.
    -   Mounts the `src` directory into the container.

-   **`localstack` service**:
    -   Provides local emulation of AWS services (like S3).
    -   Persists data in a Docker volume named `localstack_data`.
    -   Exposes the LocalStack dashboard on port `8080`.

-   **`init-aws` service**:
    -   A one-off job that runs the `init-aws.sh` script to create the S3 bucket on startup.

### Development Environment (Dev Containers)

The `.devcontainer/devcontainer.json` file configures VS Code to develop inside a container.

-   It uses the `docker-compose.yml` to define the environment, connecting to the `dashboard` service.
-   It forwards ports `8501` (dashboard) and `8080` (LocalStack UI).
-   It keeps the container running with an infinite sleep command.
-   It installs the recommended Python extension.

## How to Run and Debug

### Running the Application

To run the entire application, use Docker Compose:

```bash
docker compose up
```

This will start all services. The `analyzer` will run, and then you can access the `dashboard` at [http://localhost:8501](http://localhost:8501).

### Running Services Individually

You can also run the services individually using the CLI in `main.py`:

-   **To run the analysis:**
    ```bash
    python main.py analyze
    ```

-   **To run the dashboard:**
    ```bash
    python main.py dashboard
    ```

### Debugging

When using the Dev Container, VS Code will be attached to the `dashboard` service container. You can use the integrated debugger to set breakpoints and debug the `dashboard.py` application.
