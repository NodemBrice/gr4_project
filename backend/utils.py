# backend/utils.py
from typing import Dict, Any
import pandas as pd
from pathlib import Path

def load_profiles(path: str = "profiles.xlsx") -> Dict[str, Dict[str, Any]]:
    """
    Reads an Excel file with columns: email, niveau, tone (optional)
    Returns a dict keyed by email -> profile data.
    """
    p = Path(path)
    if not p.exists():
        return {}
    df = pd.read_excel(p)
    profiles = {}
    for _, row in df.iterrows():
        email = str(row.get("email", "")).strip()
        if not email:
            continue
        profiles[email.lower()] = {
            "niveau": str(row.get("niveau", "intermediate")),
            "tone": str(row.get("tone", "neutral")),
            "name": str(row.get("name", "")) if "name" in row else "",
        }
    return profiles

def find_profile_for_email(email: str, path: str = "profiles.xlsx"):
    profiles = load_profiles(path)
    return profiles.get(email.lower())