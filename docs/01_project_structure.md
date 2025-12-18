# Project Structure and Infrastructure

This document provides an overview of the project structure, Docker setup, and development environment.

## High-Level Architecture

The project is an "Agentic Operational Intelligence System" designed to analyze operational data and present it through a web dashboard. It consists of two main services orchestrated by Docker Compose:

1.  **`analyzer`**: A batch job that runs a `crewai`-based agentic crew to perform data analysis.
2.  **`dashboard`**: A Streamlit web application that visualizes the results from the `analyzer`.

These services communicate via a shared Docker volume named `shared_data`.

## Directory Structure

```
ops-intelligence/
├── .devcontainer/
│   └── devcontainer.json   # VS Code Dev Container configuration
├── .env                    # Environment variables
├── .gitignore
├── docker-compose.yml      # Docker Compose for service orchestration
├── Dockerfile              # Docker image definition for the services
├── pyproject.toml          # Python project metadata and dependencies
├── README.md
├── requirements.txt        # Python dependencies
├── docs/                   # Project documentation
└── src/
    ├── ops_intelligence/   # Source code for the 'analyzer' service
    │   ├── config/
    │   │   ├── agents.yaml # Agent definitions
    │   │   └── tasks.yaml  # Task definitions
    │   ├── tools/          # Custom tools for agents
    │   ├── crew.py         # Crew definition and task orchestration
    │   └── main.py         # Entry point for the application (CLI)
    └── web/
        └── dashboard.py    # Source code for the Streamlit 'dashboard'
```

## Infrastructure Setup

### Docker

The entire application is containerized, and the setup is defined in `Dockerfile` and `docker-compose.yml`.

#### `Dockerfile`

The `Dockerfile` defines the common image for both the `analyzer` and `dashboard` services. It starts from a Python 3.11 base image, installs the dependencies listed in `requirements.txt`, and sets up the working directory.

#### `docker-compose.yml`

The `docker-compose.yml` file orchestrates the multi-service application:

-   **`analyzer` service**:
    -   Builds from the `Dockerfile` in the current directory.
    -   Runs the command `python -m src.ops_intelligence.main analyze` to start the analysis process.
    -   Mounts the `shared_data` volume to `/app/data` to store the output JSON.
    -   Mounts the `src` directory into the container for development.

-   **`dashboard` service**:
    -   Also builds from the same `Dockerfile`.
    -   Runs the command `python -m src.ops_intelligence.main dashboard` to start the web server.
    -   Depends on the `analyzer` service to ensure the analysis runs first.
    -   Exposes port `8501` for the Streamlit dashboard.
    -   Mounts the `shared_data` volume to `/app/data` to read the analysis results.
    -   Mounts the `src` directory into the container.

-   **`shared_data` volume**:
    -   A named volume that enables data sharing between the `analyzer` and `dashboard` services.

### Development Environment (Dev Containers)

The `.devcontainer/devcontainer.json` file provides a configuration for Visual Studio Code to develop inside a container. This ensures a consistent and reproducible development environment.

-   It uses the `docker-compose.yml` to define the environment.
-   It specifies the `dashboard` service as the one to connect to.
-   It forwards port `8501` for accessing the dashboard.
-   It sets the sleep command to `infinity` to keep the container running.
-   It installs the recommended Python extension for VS Code.

## How to Run and Debug

### Running the Application

To run the entire application, use Docker Compose:

```bash
docker compose up
```

This will first run the `analyzer` service. Once it completes, the `dashboard` service will start, and you can access the web interface at [http://localhost:8501](http://localhost:8501).

### Running Services Individually

You can also run the services individually using the CLI defined in `src/ops_intelligence/main.py`.

-   **To run the analysis:**
    ```bash
    python -m main analyze
    ```

-   **To run the dashboard:**
    ```bash
    python -m main dashboard
    ```

### Debugging

When using the Dev Container, VS Code will be attached to the `dashboard` service container. You can use the integrated debugger to set breakpoints and debug the `dashboard.py` application.
