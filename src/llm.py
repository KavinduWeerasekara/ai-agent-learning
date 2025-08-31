from dotenv import load_dotenv
import os
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()

def get_llm_model() -> OpenAIModel:
    """
    Return an OpenAI-compatible model for Pydantic-AI.
    Works with Ollama/OpenAI/OpenRouter via your .env.
    """
    llm = os.getenv("LLM_CHOICE", "gqwen2.5:7b-instruct-q4_K_M")
    base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    api_key = os.getenv("LLM_API_KEY", "ollama")  # Ollama ignores it
    provider = OpenAIProvider(base_url=base_url, api_key=api_key)
    return OpenAIModel(llm, provider=provider)
