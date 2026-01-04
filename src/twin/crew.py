import os
import yaml
from crewai import Crew, Agent, Task, LLM
from twin.tools.serper_tool import search

BASE_DIR = os.path.dirname(__file__)
CONFIG_DIR = os.path.join(BASE_DIR, "config")

# Load YAML
with open(os.path.join(CONFIG_DIR, "agents.yaml")) as f:
    agent_cfg = yaml.safe_load(f)

with open(os.path.join(CONFIG_DIR, "tasks.yaml")) as f:
    task_cfg = yaml.safe_load(f)

# Groq LLM
llm = LLM(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url=os.getenv("GROQ_API_BASE"),
    model=os.getenv("GROQ_MODEL_NAME"),
)

# Create agents
agents = {
    name: Agent(**cfg, llm=llm)
    for name, cfg in agent_cfg.items()
}

def build_twin_crew(company: str):

    # Live market context
    market_data = search(f"{company} product roadmap pricing leaks future plans")

    context = f"""
    Live market intelligence for {company}:
    {market_data}
    """

    tasks = [
        Task(
            description=task_cfg["behavior_task"]["description"].format(company=company) + context,
            expected_output=task_cfg["behavior_task"]["expected_output"],
            agent=agents["behavior_modeler"],
        ),
        Task(
            description=task_cfg["roadmap_task"]["description"].format(company=company) + context,
            expected_output=task_cfg["roadmap_task"]["expected_output"],
            agent=agents["roadmap_predictor"],
        ),
        Task(
            description=task_cfg["pricing_task"]["description"].format(company=company) + context,
            expected_output=task_cfg["pricing_task"]["expected_output"],
            agent=agents["pricing_predictor"],
        ),
        Task(
            description=task_cfg["launch_task"]["description"].format(company=company) + context,
            expected_output=task_cfg["launch_task"]["expected_output"],
            agent=agents["launch_engine"],
        ),
    ]

    return Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=True
    )
