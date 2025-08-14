# src/resume_tailor/emergent_adapter.py
import os
import requests

def polish_with_emergent(draft_text, api_url=None, api_key=None, model=None, max_tokens=512):
    """
    Polishes resume text using Emergent.sh free-tier API.
    Assumes API follows OpenAI-compatible chat-completions schema.
    """
    api_url = api_url or os.environ.get("EMERGENT_API_URL")
    api_key = api_key or os.environ.get("EMERGENT_API_KEY")
    model = model or os.environ.get("EMERGENT_MODEL", "gpt-3.5-turbo")

    if not api_key or not api_url:
        raise ValueError("EMERGENT_API_KEY or EMERGENT_API_URL not set in environment")

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a resume polisher. RULES: "
                    "(1) Do not add or invent any facts, numbers, or claims. "
                    "(2) Only rephrase and clean wording for ATS and human readability. "
                    "(3) Keep bullets, section headers, and keywords. "
                    "(4) Preserve existing numbers."
                )
            },
            {
                "role": "user",
                "content": draft_text
            }
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    resp = requests.post(api_url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # Emergent API may follow OpenAI's format
    if "choices" in data and isinstance(data["choices"], list):
        choice = data["choices"][0]
        if "message" in choice and "content" in choice["message"]:
            return choice["message"]["content"].strip()

    # fallback: try top-level text field
    if "text" in data:
        return data["text"]

    return str(data)
