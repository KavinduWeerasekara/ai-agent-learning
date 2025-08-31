import asyncio
from pydantic_ai import Agent
from src.llm import get_llm_model
from src.prompt import AGENT_SYSTEM_PROMPT

# Build the agent once (no tools yet)
agent = Agent(get_llm_model(), system_prompt=AGENT_SYSTEM_PROMPT, retries=0)

async def run_agent_async(question: str) -> dict:
    """
    Run the LLM agent with a plain question.
    Returns a JSON-serializable dict: {"ok": True, "answer": "..."}
    """
    result = await agent.run(question)
    return {"ok": True, "answer": result.output}

def run_agent(question: str) -> dict:
    """
    Sync entry point (wraps the async runner with asyncio.run).
    """
    return asyncio.run(run_agent_async(question))
