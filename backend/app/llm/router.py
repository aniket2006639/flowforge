from app.llm.fastrouter_client import FastRouterClient
from app.llm.ollama_client import OllamaClient
from app.llm.openai_client import OpenAIClient


def get_llm_client(provider: str | None = None):
    if provider == "ollama":
        return OllamaClient()
    elif provider == "openai":
        return OpenAIClient()
    else:
        # ✅ DEFAULT
        return FastRouterClient()
