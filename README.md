# Projet2_gpa
Gestion de Notes

Projet de gestion des notes des élèves avec un backend en **Python typé**, un frontend simple en HTML/CSS/JS et un workflow automatisé de validation de code.

---

## 📂 Structure du projet

gestion-notes/
│
├── .github/
│ └── workflows/
│ └── code-check.yml # Workflow GitHub Actions pour validation automatique
│
├── backend/
│ ├── app.py # Point d'entrée Flask (API)
│ ├── notes.py # Gestion des notes
│ ├── eleves.py # Gestion des élèves
│ ├── utils.py # Fonctions utilitaires
│ ├── email_sender.py # Envoi de mails automatiques (optionnel)
│ └── ai_formatter.py # Formatage intelligent (optionnel)
│
├── frontend/
│ ├── index.html # Page d'accueil
│ ├── notes.html # Page pour afficher les notes
│ ├── style.css # Styles CSS
│ └── script.js # Scripts JS
│
├── mypy.ini # Configuration pour mypy
├── .pylintrc # Configuration pour pylint
├── eslint.config.js # Configuration ESLint (JS)
├── .htmlhintrc # Configuration HTMLHint
├── requirements.txt # Dépendances Python
└── README.md


---

## ⚡ Technologies et outils utilisés

- **Python 3.13** (backend typé avec `mypy`)
- **Flask** pour l’API backend
- **HTML/CSS/JS** pour le frontend
- **ESLint** pour valider le JavaScript
- **HTMLHint** pour valider le HTML
- **Pylint** pour la qualité du code Python
- **GitHub Actions** pour automatiser la validation de code à chaque push ou pull request

---

## 💻 Installation et mise en place

### 1. Cloner le dépôt

 bash
git clone git@github.com:NodemBrice/Projet2_gpa.git
cd Projet2_gpa

2. Créer et activer l'environnement virtuel Python
bash

python -m venv venv

# Windows Git Bash
source venv/Scripts/activate
3. Installer les dépendances Python
bash

pip install -r requirements.txt
4. Installer Node.js et les outils JS
Installer Node.js depuis nodejs.org

Installer les packages globaux pour le projet :

bash

npm install -g htmlhint eslint
5. Vérifier les outils
bash

# Python
python --version
# Flask
python -m flask --version
# ESLint
eslint -v
# HTMLHint
htmlhint -v
🚀 Lancer le backend
bash

python backend/app.py
L’API sera disponible sur http://127.0.0.1:5000/

🌐 Lancer le frontend
Ouvre les fichiers HTML dans frontend/ directement dans ton navigateur.

✅ Workflow GitHub Actions
Le workflow code-check.yml automatise la validation du code à chaque push ou pull request :

mypy → vérifie le typage Python

pylint → analyse la qualité du code Python

HTMLHint → analyse le HTML

ESLint → analyse le JavaScript

⚠️ Si une règle est violée, le workflow échoue et les détails sont visibles dans l’onglet Actions du dépôt GitHub.

🔧 Règles de codage appliquées
Pas d’import inutile en Python et JS

Typage strict en Python (mypy)

Lignes JS max 120 caractères

Obligatoire : guillemets doubles et ; pour le JS

Lignes Python max 100 caractères (configurable via pylint)

🧪 Tests
Les tests unitaires Python sont dans le dossier tests/

Pour lancer les tests :

bash
Copier le code
python -m unittest discover tests
👥 Contribution
Créer une branche pour chaque fonctionnalité ou bugfix :

bash
Copier le code
git checkout -b feature/nom-de-fonctionnalité
Valider le code localement avec :

bash
Copier le code
mypy backend/
pylint backend/
eslint "frontend/**/*.js"
htmlhint frontend/
Commit & push :

bash
Copier le code
git add .
git commit -m "Description du commit"
git push origin feature/nom-de-fonctionnalité
Ouvrir une Pull Request pour revue avant fusion dans main.

📌 Notes supplémentaires
Respecter les règles de typage et de style permet à GitHub Actions de valider automatiquement votre code.

Tout code qui ne respecte pas les règles déclenche un workflow rouge, signalant les erreurs à corriger.

Ce README doit être votre guide de référence pour travailler sur le projet.

yaml
Copier le code

--- commandes installation des dependance du fichier setup_hooks.sh
 chmod +x setup_hooks.sh
 ./setup_hooks.sh
 il yaura execution du fichier et installation des deendances necessaires au projet
