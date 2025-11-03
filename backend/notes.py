from flask import Flask, jsonify, request
# Changement d'import : utilise l'import direct puisque 'notes.py' est dans le même dossier

from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv() # Pour charger les variables d'environnement

# Fichier : C:\Users\NDONGO\gr4_project\backend\notes.py

from typing import List, Dict, Any

# Simulation de la base de données
NOTES_DATA = [
    {"id": 1, "nom": "Alice", "matiere": "Maths", "note": 15},
    {"id": 2, "nom": "Bob", "matiere": "Physique", "note": 12},
    {"id": 3, "nom": "Charlie", "matiere": "SVT", "note": 14},
]

def get_all_notes() -> List[Dict[str, Any]]:
    """Retourne la liste complète de toutes les notes."""
    return NOTES_DATA

def add_note(nom: str, matiere: str, note: float) -> Dict[str, Any]:
    """Ajoute une nouvelle note à la liste."""
    # Logique pour attribuer un nouvel ID
    new_id = max([n['id'] for n in NOTES_DATA]) + 1 if NOTES_DATA else 1
    new_note = {"id": new_id, "nom": nom, "matiere": matiere, "note": note}
    NOTES_DATA.append(new_note)
    return new_note