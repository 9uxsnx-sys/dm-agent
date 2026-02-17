"""
LLM Service - HuggingFace Inference API (Mistral-7B-Instruct-v0.2)
Uses the OpenAI-compatible chat completions endpoint via router.huggingface.co
"""
import httpx
from app.config import settings

HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

DEFAULT_PARAMS = {
    "temperature": 0.3,
    "max_tokens": 300,
}


async def generate_response(message: str, system_instruction: str = None) -> str:
    """
    Send a prompt to HuggingFace Inference API and return the generated text.
    Uses OpenAI-compatible chat completions format.
    """
    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": message})

    headers = {
        "Authorization": f"Bearer {settings.HF_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": HF_MODEL,
        "messages": messages,
        **DEFAULT_PARAMS,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()

    result = response.json()

    # OpenAI-compatible format: choices[0].message.content
    try:
        return result["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return str(result)
