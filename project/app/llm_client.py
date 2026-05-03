import requests
from .config import LLM_BASE_URL, LLM_MODEL

def call_llm(prompt: str, temperature: float = 0.0, system: str | None = None) -> str:
    """
    Call the local Ollama model and return the full text response.
    Uses /api/generate with stream disabled for simplicity.
    """
    url = f"{LLM_BASE_URL}/api/generate"

    data = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    # Optional: add a system prompt if you want stronger control
    if system:
        data["system"] = system

    resp = requests.post(url, json=data, timeout=120)
    resp.raise_for_status()
    payload = resp.json()
    # Ollama's /api/generate returns {"model": ..., "created_at": ..., "response": "...", ...}
    return payload.get("response", "").strip()