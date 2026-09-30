"""
agents.py
---------
Defines the 4 CrewAI agents that make up FreelanceOS.
Each agent has a role, a goal, and a backstory that shapes how the LLM behaves.
"""

from crewai import Agent, LLM


def build_llm(api_key: str, model: str = "gemini-3.5-flash-lite", temperature: float = 0.4) -> LLM:
    """Create the shared Google Gemini model used by all agents (free tier works)."""
    # The "gemini/" prefix tells CrewAI (via LiteLLM) to call Google's Gemini API.
    return LLM(model=f"gemini/{model}", api_key=api_key, temperature=temperature)


def create_agents(llm: LLM) -> dict:
    """Create and return all four agents in a dictionary."""

    # 1) LEAD SCOUT: evaluates whether a job is worth pursuing
    lead_scout = Agent(
        role="Lead Scout",
        goal="Analyze freelance job postings and decide if they are a good fit and worth pursuing.",
        backstory=(
            "You are a veteran freelance talent broker who has reviewed thousands of job "
            "posts. You quickly spot the client's real needs, hidden red flags (vague scope, "
            "unrealistic budgets, scope creep) and buying signals."
        ),
        llm=llm,
        allow_delegation=False,  # keeps the workflow simple and predictable
        verbose=True,
    )

    # 2) PROPOSAL ARCHITECT: writes the winning pitch
    proposal_architect = Agent(
        role="Proposal Architect",
        goal="Write a personalized, persuasive proposal that wins the client's trust.",
        backstory=(
            "You are an award-winning copywriter who specializes in freelance proposals. "
            "You open with the client's problem (not your resume), show relevant proof, "
            "and end with a clear, low-friction call to action."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=True,
    )

    # 3) PROJECT MANAGER: turns the job into a realistic plan
    project_manager = Agent(
        role="Project Manager",
        goal="Break the project into clear milestones, timelines and deliverables.",
        backstory=(
            "You are a PMP-certified project manager who plans work for solo freelancers. "
            "You are realistic about time, include buffers, and define what 'done' means "
            "for every milestone."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=True,
    )

    # 4) FINANCE OFFICER: pricing, payment terms, invoice
    finance_officer = Agent(
        role="Finance Officer",
        goal="Create fair pricing, payment terms and an invoice draft that protect the freelancer's income.",
        backstory=(
            "You are a freelance-focused accountant. You price by value and effort, "
            "recommend deposits and milestone payments, and always include late-fee "
            "and revision policies."
        ),
        llm=llm,
        allow_delegation=False,
        verbose=True,
    )

    return {
        "lead_scout": lead_scout,
        "proposal_architect": proposal_architect,
        "project_manager": project_manager,
        "finance_officer": finance_officer,
    }
