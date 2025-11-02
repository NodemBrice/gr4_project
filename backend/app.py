from flask import Flask, render_template
from typing import Any
from backend.notes import get_all_notes

app: Flask = Flask(__name__)

@app.route("/")
def home() -> Any:
    notes = get_all_notes()
    return render_template("index.html", notes=notes)

if __name__ == "__main__":
    app.run(debug=True)
