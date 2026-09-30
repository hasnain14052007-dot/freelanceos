"""
main.py
-------
Binds the agents and tasks into a Crew and runs it.
You can run this file directly for a quick terminal test:  python main.py
"""

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crewai import Crew, Process

from agents import build_llm, create_agents
from tasks import create_tasks


class FreelanceInput(BaseModel):
    """Validates the data the user types into the app."""
    job_description: str = Field(min_length=20, description="The job posting text")
    freelancer_name: str = "Freelancer"
    skills: str = "Not specified"
    experience: str = "Not specified"
    hourly_rate: float = Field(default=50.0, gt=0)
    availability: str = "20 hours per week"


# Order of the result sections, matching the order of the tasks
SECTION_KEYS = ["lead_analysis", "proposal", "project_plan", "finance"]


def run_freelance_crew(data: FreelanceInput, api_key: str, model: str = "gemini-3.5-flash-lite") -> dict:
    """Run the full 4-agent workflow and return each agent's output as text."""
    llm = build_llm(api_key, model)
    agents = create_agents(llm)
    tasks = create_tasks(agents)

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,  # tasks run one after another
        max_rpm=8,  # stay under Gemini free-tier rate limits
        verbose=True,
    )

    # The dict keys fill the {placeholders} in tasks.py
    result = crew.kickoff(inputs=data.model_dump())

    # Collect the raw text output of each task
    outputs = {}
    for key, task_output in zip(SECTION_KEYS, result.tasks_output):
        outputs[key] = task_output.raw
    return outputs


if __name__ == "__main__":
    load_dotenv()
    demo = FreelanceInput(
        job_description="Looking for a Python developer to build a web scraper that collects "
                        "product prices from 5 e-commerce sites and exports to Google Sheets.",
        freelancer_name="Alex",
        skills="Python, web scraping, APIs",
        experience="3 years freelancing",
        hourly_rate=45,
    )
    for name, text in run_freelance_crew(demo, os.getenv("GEMINI_API_KEY", "")).items():
        print(f"\n===== {name.upper()} =====\n{text}")
