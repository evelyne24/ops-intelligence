# CrewAI Setup

The core of the `analyzer` service is a `crewai`-based system defined in `src/ops_intelligence/crew.py`. This file sets up the agents, tasks, and the crew that orchestrates the analysis process.

## Crew Definition

The `OpsIntelligenceCrew` class inherits from `CrewBase` and defines the components of the crew.

```python
@CrewBase
class OpsIntelligenceCrew:
    """OpsIntelligence crew"""
    
    # Paths to YAML configs
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ... (initialization)

    @agent
    def data_engineer(self) -> Agent:
        # ...

    @agent
    def ops_analyst(self) -> Agent:
        # ...

    @task
    def ingestion_task(self) -> Task:
        # ...

    @task
    def analysis_task(self) -> Task:
        # ...

    @crew
    def crew(self) -> Crew:
        # ...
```

## Language Model

The crew uses the `gemini/gemini-pro` model from Google, configured in the `__init__` method of the `OpsIntelligenceCrew` class. The API key is retrieved from the `GEMINI_API_KEY` environment variable.

## Agents

The crew consists of two agents, each with a specific role:

1.  **`data_engineer`**: This agent is responsible for data ingestion. It uses the `EngineeringSimulatorTool`.
2.  **`ops_analyst`**: This agent is responsible for analyzing the data and calculating metrics. It uses the `MetricsCalculatorTool`.

The configurations for these agents (their role, goal, and backstory) are loaded from the `config/agents.yaml` file.

## Tasks

The crew performs two sequential tasks:

1.  **`ingestion_task`**: This is the first task, likely handled by the `data_engineer` agent to simulate or fetch engineering data.
2.  **`analysis_task`**: This task follows the ingestion task. It is likely performed by the `ops_analyst` to process the data and generate insights. The output of this task is saved to a file named `dashboard_data.json`.

The descriptions for these tasks are loaded from the `config/tasks.yaml` file.

## Crew Execution

The `crew` method defines the crew's execution process.

```python
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
```

The crew is configured to run in a sequential process, meaning the tasks are executed one after the other in the order they are defined. The `verbose=True` setting ensures detailed logging of the crew's execution.
