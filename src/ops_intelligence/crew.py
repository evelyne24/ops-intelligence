import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.ops_intelligence.tools.simulator import EngineeringSimulatorTool
from src.ops_intelligence.tools.calculator import MetricsCalculatorTool
from pathlib import Path

@CrewBase
class OpsIntelligenceCrew:
    """OpsIntelligence crew"""

    base_path = Path(__file__).parent
    
    # Paths to YAML configs
    agents_config = str(base_path / 'config' / 'agents.yaml')
    tasks_config = str(base_path / 'config' / 'tasks.yaml')

    def __init__(self):
        self.gemini_llm = LLM(
            model="gemini/gemini-2.5-flash-lite",
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.2
        )

    @agent
    def data_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['data_engineer'],
            tools=[EngineeringSimulatorTool()],
            llm=self.gemini_llm,
            verbose=True
        )

    @agent
    def ops_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['ops_analyst'],
            tools=[MetricsCalculatorTool()],
            llm=self.gemini_llm,
            verbose=True
        )

    @task
    def ingestion_task(self) -> Task:
        return Task(config=self.tasks_config['ingestion_task'], 
                    agent=self.data_engineer())

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'],
            agent=self.ops_analyst(),
            output_file='dashboard_data.json' # Saves output to root
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.data_engineer(), self.ops_analyst()],
            tasks=[self.ingestion_task(), self.analysis_task()],
            process=Process.sequential,
            verbose=True,
            output_log_file="crew_execution.log"
        )