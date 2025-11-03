from dataclasses import dataclass
from typing import Optional, List
import json
from pathlib import Path

ELEVE_FILE = Path("backend/_eleves_store.json")

@dataclass
class Eleve:
    id: int
    nom: str
    email: str
    niveau: str  # ex: beginner/intermediate/advanced

def _load() -> List[dict]:
    if not ELEVE_FILE.exists():
        return []
    try:
        return json.loads(ELEVE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError):
        print("Error loading eleves file, returning empty list.")
        return []

def _save(data: List[dict]) -> None:
    ELEVE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")

def list_eleves() -> List[Eleve]:
    return [Eleve(**d) for d in _load()]

def add_eleve(nom: str, email: str, niveau: str = "beginner") -> Eleve:
    items = _load()
    nxt = max((d["id"] for d in items), default=0) + 1
    e = {"id": nxt, "nom": nom, "email": email, "niveau": niveau}
    items.append(e)
    _save(items)
    return Eleve(**e)

def get_eleve(eid: int) -> Optional[Eleve]:
    for d in _load():
        if d["id"] == eid:
            return Eleve(**d)
    return None

def update_eleve(eid: int, nom: str, email: str, niveau: str) -> Optional[Eleve]:
    items = _load()
    for i, d in enumerate(items):
        if d["id"] == eid:
            items[i] = {"id": eid, "nom": nom, "email": email, "niveau": niveau}
            _save(items)
            return Eleve(**items[i])
    return None

def delete_eleve(eid: int) -> bool:
    items = _load()
    new = [d for d in items if d["id"] != eid]
    if len(new) == len(items):
        return False
    _save(new)
    return True