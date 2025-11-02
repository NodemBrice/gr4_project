from typing import List, Dict, Any

def get_all_notes() -> List[Dict[str, Any]]:
    """Retourne une liste de notes simulées."""
    notes = [
        {"nom": "Alice", "matiere": "Maths", "note": 15},
        {"nom": "Bob", "matiere": "Physique", "note": 12},
        {"nom": "Charlie", "matiere": "SVT", "note": 14},
    ]
    return notes
