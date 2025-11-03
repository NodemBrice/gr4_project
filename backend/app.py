# Fichier : C:\Users\NDONGO\gr4_project\backend\app.py

from flask import Flask, jsonify, request
# Import local de notes.py (qui est dans le même dossier)
from .notes import get_all_notes, add_note 
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
app: Flask = Flask(__name__)
CORS(app)

# --- Routes d'API pour les notes ---
@app.route("/api/notes", methods=["GET"])
def api_get_notes():
    """Récupère toutes les notes."""
    notes = get_all_notes()
    return jsonify(notes)

@app.route("/api/notes", methods=["POST"])
def api_add_note():
    """Ajoute une nouvelle note."""
    data = request.get_json()
    try:
        nom = data["nom"]
        matiere = data["matiere"]
        note = float(data["note"])    
        
        new_note = add_note(nom, matiere, note)
        
        return jsonify(new_note), 201
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Données manquantes ou format incorrect"}), 400

# --- Autre route API (NDONGO) ---
@app.route('/api/NDONGO')
def api_ndongo():
    return jsonify({
        "message": "Hello NDONGO",
        "key_exists": bool(os.getenv("API_KEY_NDONGO"))
    })

@app.route("/")
def home():
    return "API running. Visitez /api/notes ou ouvrez le frontend/notes.html."

if __name__ == "__main__":
    app.run(debug=True)