from __future__ import annotations

from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai_tools import SerperDevTool

from .tools.serper_shopping import serper_shopping_candidates

from .schemas.recommendation import RecommendationOutput
from .services.guardrails import validate_inputs


@CrewBase
class ShoppingAssistantCrew:
    """ShoppingAssistantCrew: Planner → Research → Compare → Final."""

    agents: List[BaseAgent]
    tasks: List[Task]

    @before_kickoff
    def _guardrails(self, inputs):
        # Validate inputs early (and block unsafe categories).
        return validate_inputs(inputs)

    @agent
    def planner(self) -> Agent:
        return Agent(
            config=self.agents_config["planner"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def researcher(self) -> Agent:
        # Web search tool (Serper). If SERPER_API_KEY is missing, the tool may fail —
        # keep it in place so you can add the key and immediately get web capability.
        return Agent(
            config=self.agents_config["researcher"],  # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool(), serper_shopping_candidates],
        )

    @agent
    def comparer(self) -> Agent:
        return Agent(
            config=self.agents_config["comparer"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def final_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config["final_advisor"],  # type: ignore[index]
            verbose=True,
        )

    @task
    def plan_task(self) -> Task:
        return Task(config=self.tasks_config["plan_task"])  # type: ignore[index]

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])  # type: ignore[index]

    @task
    def compare_task(self) -> Task:
        return Task(config=self.tasks_config["compare_task"])  # type: ignore[index]

    @task
    def finalize_task(self) -> Task:
        # If you want structured output, uncomment output_pydantic.
        return Task(
            config=self.tasks_config["finalize_task"],  # type: ignore[index]
            output_file="output/recommendation.md",
            # output_pydantic=RecommendationOutput,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # auto-collected
            tasks=self.tasks,    # auto-collected
            process=Process.sequential,
            verbose=True,
            # memory=True,  # enable if you want built-in memory
        )
