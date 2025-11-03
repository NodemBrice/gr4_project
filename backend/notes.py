from dataclasses import dataclass
from typing import List, Optional
import json
from pathlib import Path

DATA_FILE = Path("backend/_notes_store.json")

@dataclass
class Note:
    id: int
    title: str
    content: str

def _load_store() -> List[dict]:
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError):
        return []

def _save_store(items: List[dict]) -> None:
    DATA_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=4), encoding="utf-8")

def get_all_notes() -> List[Note]:
    raw = _load_store()
    return [Note(**r) for r in raw]

def _next_id(items: List[dict]) -> int:
    if not items:
        return 1
    return max(item["id"] for item in items) + 1

def add_note(title: str, content: str) -> Note:
    items = _load_store()
    nid = _next_id(items)
    note = {"id": nid, "title": title, "content": content}
    items.append(note)
    _save_store(items)
    return Note(**note)

def get_note(note_id: int) -> Optional[Note]:
    items = _load_store()
    for r in items:
        if r["id"] == note_id:
            return Note(**r)
    return None

def update_note(note_id: int, title: str, content: str) -> Optional[Note]:
    items = _load_store()
    for i, r in enumerate(items):
        if r["id"] == note_id:
            items[i] = {"id": note_id, "title": title, "content": content}
            _save_store(items)
            return Note(**items[i])
    return None

def delete_note(note_id: int) -> bool:
    items = _load_store()
    new = [r for r in items if r["id"] != note_id]
    if len(new) == len(items):
        return False
    _save_store(new)
    return True