# CrewAI Setup

The core of the `analyzer` service is a `crewai`-based system defined in `src/ops_intelligence/crew.py`. This file sets up the agents, tasks, and the crew that orchestrates the analysis process.

## Crew Definition

The `OpsIntelligenceCrew` class inherits from `CrewBase` and defines the components of the crew.

```python
@CrewBase
class OpsIntelligenceCrew:
    """OpsIntelligence crew"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        self.gemini_llm = LLM(
            model="gemini/gemini-2.5-flash-lite",
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.2
        )

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

The crew uses the `gemini/gemini-2.5-flash-lite` model from Google, configured in the `__init__` method of the `OpsIntelligenceCrew` class. The API key is retrieved from the `GEMINI_API_KEY` environment variable, and the `temperature` is set to `0.2` for more predictable outputs.

## Agents

The crew consists of two agents, each with a specific role:

1.  **`data_engineer`**: Responsible for data ingestion, using the `EngineeringSimulatorTool`.
2.  **`ops_analyst`**: Responsible for analyzing the data and calculating metrics, using the `MetricsCalculatorTool`.

The configurations for these agents (role, goal, backstory) are loaded from `config/agents.yaml`.

## Tasks

The crew performs two sequential tasks:

1.  **`ingestion_task`**: Handled by the `data_engineer` agent to simulate engineering data.
2.  **`analysis_task`**: Performed by the `ops_analyst` to process the data and generate insights. The output of this task is saved to a file named `dashboard_data.json` in the project's root directory.

The descriptions for these tasks are loaded from `config/tasks.yaml`.

## Crew Execution

The `crew` method defines the crew's execution process.

```python
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.data_engineer(), self.ops_analyst()],
            tasks=[self.ingestion_task(), self.analysis_task()],
            process=Process.sequential,
            verbose=True,
            output_log_file="crew_execution.log"
        )
```

The crew is configured to run in a sequential process. `verbose=True` ensures detailed logging, and the execution log is saved to `crew_execution.log`.
