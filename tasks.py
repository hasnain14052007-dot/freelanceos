"""
tasks.py
--------
Defines one task per agent. Tasks run in order, and each later task receives
the earlier tasks' output through `context=[...]`.

Placeholders like {job_description} are filled in by crew.kickoff(inputs=...).
"""

from crewai import Task


def create_tasks(agents: dict) -> list:
    """Create the 4 sequential tasks and return them in execution order."""

    # TASK 1: Lead Scout analyzes the job post
    scout_task = Task(
        description=(
            "Analyze this freelance job posting for a freelancer.\n\n"
            "JOB POSTING:\n{job_description}\n\n"
            "FREELANCER PROFILE:\n"
            "- Name: {freelancer_name}\n"
            "- Skills: {skills}\n"
            "- Experience: {experience}\n\n"
            "Provide: (1) a short summary of what the client really wants, "
            "(2) a fit score from 1-10 with reasoning, (3) red flags, "
            "(4) opportunities, (5) a clear GO / NO-GO recommendation."
        ),
        expected_output="A markdown lead analysis with summary, fit score, red flags, opportunities and GO/NO-GO.",
        agent=agents["lead_scout"],
    )

    # TASK 2: Proposal Architect writes the proposal (uses the scout's analysis)
    proposal_task = Task(
        description=(
            "Using the lead analysis, write a winning proposal from {freelancer_name}.\n"
            "Keep it under 300 words. Start with the client's problem, highlight the most "
            "relevant skills ({skills}), outline the approach briefly, and end with a "
            "friendly call to action. Address any red flags tactfully with clarifying questions."
        ),
        expected_output="A ready-to-send proposal in markdown, under 300 words.",
        agent=agents["proposal_architect"],
        context=[scout_task],
    )

    # TASK 3: Project Manager builds the plan
    pm_task = Task(
        description=(
            "Create a project plan for this job, assuming availability of: {availability}.\n"
            "Include: milestones with deliverables, estimated hours per milestone, "
            "a week-by-week timeline, key risks with mitigations, and a communication cadence. "
            "Present the milestones as a markdown table."
        ),
        expected_output="A markdown project plan with a milestone table, timeline, risks and communication plan.",
        agent=agents["project_manager"],
        context=[scout_task, proposal_task],
    )

    # TASK 4: Finance Officer prices it and drafts an invoice
    finance_task = Task(
        description=(
            "Using the project plan's hour estimates and the freelancer's hourly rate of "
            "${hourly_rate}/hour, produce: (1) a recommended fixed price vs hourly price "
            "comparison, (2) a payment schedule (deposit + milestones), (3) a first-invoice "
            "draft for {freelancer_name} with line items and totals, and (4) terms "
            "(late fees, revision limits). Show the math clearly."
        ),
        expected_output="A markdown finance package: pricing comparison, payment schedule, invoice draft and terms.",
        agent=agents["finance_officer"],
        context=[scout_task, pm_task],
    )

    # Order matters: CrewAI runs them sequentially in this order.
    return [scout_task, proposal_task, pm_task, finance_task]
