import os
from typing import Dict, Optional
import requests

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def _local_fallback(profile: Dict[str, str], summary: str) -> str:
    # Simple heuristic fallback if no API key
    niveau = profile.get("niveau", "intermediate")
    if niveau == "beginner":
        prefix = "Bonjour,\n\nJ'ai regardé votre code et voici des explications claires et pédagogiques :\n\n"
    elif niveau == "advanced":
        prefix = "Salut,\n\nVoici un bref résumé technique des problèmes détectés :\n\n"
    else:
        prefix = "Bonjour,\n\nRésumé des problèmes détectés :\n\n"
    return prefix + summary

def ai_rephrase(profile: Dict[str, str], summary: str) -> Optional[str]:
    """Return a human-friendly reformulation (uses OpenAI if API key present)."""
    if not OPENAI_KEY:
        return _local_fallback(profile, summary)

    profile_str = f"Niveau: {profile.get('niveau', 'unknown')}, Nom: {profile.get('nom', 'unknown')}"
    prompt = (
        f"You are a helpful assistant. The recipient profile is: {profile_str}.\n"
        f"Please rewrite the following technical report into a polite, clear email adapted to the profile:\n\n{summary}\n\n"
        "Keep it concise and include actionable suggestions."
    )
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
    body = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 600,
        "temperature": 0.2,
    }
    try:
        r = requests.post(url, headers=headers, json=body, timeout=30)
        r.raise_for_status()
        data = r.json()
        text = data["choices"][0]["message"]["content"]
        return text
    except requests.RequestException as e:
        print(f"Error with OpenAI API: {e}")
        return None  # Or fallback to _local_fallback