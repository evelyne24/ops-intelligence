# Agents and Tools

This document details the agents, their tools, and the tasks they perform in the `crewai` setup.

## Agents

The crew is composed of two agents defined in `src/ops_intelligence/crew.py` and configured in `config/agents.yaml`.

### `data_engineer`

-   **Role**: Senior Data Engineer
-   **Goal**: Generate and ingest simulated operational data.
-   **Backstory**: Responsible for the integrity of the data pipeline, using a simulation tool to create a dataset representing a software team struggling with process issues.
-   **Tool**: `EngineeringSimulatorTool`

### `ops_analyst`

-   **Role**: Operational Metrics Analyst
-   **Goal**: Identify process friction (Churn and Ghost Work).
-   **Backstory**: A metrics expert who takes raw data and calculates specific friction points, strictly outputting valid JSON for the dashboard.
-   **Tool**: `MetricsCalculatorTool`

## Tools

The agents use custom tools to perform their tasks.

### `EngineeringSimulatorTool`

-   **File**: `src/ops_intelligence/tools/simulator.py`
-   **Name**: Simulated Data Generator
-   **Description**: Generates 90 days of simulated Jira/GitHub data for a struggling team.

This tool simulates data for a team of 8 engineers over 90 days, creating realistic scenarios of operational friction:

-   **Unclear Requirements (Churn)**: Some Jira tickets are marked as "churny," resulting in a higher number of "churn_events" and longer coding times.
-   **Poor Hygiene (Long Reviews)**: Some GitHub pull requests have extended review cycles, leading to longer resolution times and more comments.
-   **Ghost Work (Missing Linkage)**: Some pull requests are created without a corresponding Jira ticket reference in their title, making them "ghost" PRs.

The tool outputs a JSON string containing two lists: `jira_tickets` and `github_prs`.

### `MetricsCalculatorTool`

-   **File**: `src/ops_intelligence/tools/calculator.py`
-   **Name**: Metrics Calculator
-   **Description**: Calculates Cycle Time, Churn, and Ghost Work stats from raw JSON.

This tool takes the JSON output from the `EngineeringSimulatorTool` and performs the following calculations:

-   **Ghost Work**: Identifies pull requests where the title does not match the Jira ticket pattern (`[A-Z]+-\d+`).
-   **Churn**: Identifies Jira tickets with more than one "churn_event".

The tool then calculates summary statistics, including the percentage of ghost work and the count of high-churn tickets. The final output is a JSON object containing a `summary` and the raw data.

## Tasks

The agents execute two sequential tasks defined in `src/ops_intelligence/crew.py` and configured in `config/tasks.yaml`.

### `ingestion_task`

-   **Description**: Run the `EngineeringSimulatorTool` to fetch the last 90 days of Jira and GitHub data.
-   **Expected Output**: A raw JSON string containing `jira_tickets` and `github_prs`.
-   **Assigned Agent**: `data_engineer`

### `analysis_task`

-   **Description**: Take the raw data from the ingestion task and use the `MetricsCalculatorTool` to process it, calculating the Ghost Work percentage and Ticket Churn counts.
-   **Expected Output**: A valid JSON string containing the keys: `summary`, `raw_tickets`, and `raw_prs`.
-   **Assigned Agent**: `ops_analyst`
