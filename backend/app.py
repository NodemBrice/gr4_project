from flask import Flask, jsonify, request, abort
from typing import Any, Dict
import os

from backend.notes import get_all_notes, add_note, get_note, update_note, delete_note
from backend.eleves import list_eleves, add_eleve, get_eleve

app = Flask(__name__)

@app.route("/api/notes", methods=["GET"])
def api_list_notes():
    notes = get_all_notes()
    return jsonify([n.__dict__ for n in notes])

@app.route("/api/notes", methods=["POST"])
def api_add_note():
    data = request.get_json(force=True)
    title = data.get("title")
    content = data.get("content", "")
    if not title:
        abort(400, "Missing title")
    n = add_note(title, content)
    return jsonify(n.__dict__), 201

@app.route("/api/notes/<int:note_id>", methods=["GET"])
def api_get_note(note_id: int):
    n = get_note(note_id)
    if not n:
        abort(404)
    return jsonify(n.__dict__)

@app.route("/api/eleves", methods=["GET"])
def api_eleves():
    els = list_eleves()
    return jsonify([e.__dict__ for e in els])

@app.route("/api/eleves", methods=["POST"])
def api_add_eleve():
    data = request.get_json(force=True)
    name = data.get("nom")
    email = data.get("email")
    niveau = data.get("niveau", "beginner")
    if not name or not email:
        abort(400, "Missing name or email")
    e = add_eleve(name, email, niveau)
    return jsonify(e.__dict__), 201

if __name__ == "__main__":
    # Only run when executed as module: python -m backend.app
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("DEBUG", "False") == "True")