import argparse
import json
import os
import random
import subprocess
import sys
import smtplib

import requests
import google.generativeai as genai
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
COLLAB_EMAIL = os.getenv('COLLAB_EMAIL', 'default@example.com')
COLLAB_NAME = os.getenv('GITHUB_ACTOR', 'Collaborateur')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY', 'NodemBrice/gr4_project')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


def get_changed_files(files_from_args=None):
    if files_from_args:
        return [f for f in files_from_args if f.endswith(('.py', '.html', '.htm', '.js', '.jsx'))]
    diff = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', '--diff-filter=AM'],
        capture_output=True,
        text=True,
        check=True
    )
    return [f for f in diff.stdout.strip().split('\n') if f.endswith(('.py', '.html', '.htm', '.js', '.jsx'))]


def load_standards():
    return "Règles via Pylint (Python), HTMLHint (HTML) et ESLint (JS). Vérification IA complémentaire sur syntaxe, types et erreurs."


def analyze_with_gemini(code, standards, file_path):
    lang = file_path.split('.')[-1]
    prompt = (
        "Analyse ce code " + lang.upper() + " (" + file_path + ") :\n"
        "- Vérifie la syntaxe et erreurs potentielles.\n"
        "- Vérifie les types de variables (strict : int, float, str, list, etc. ; pas de 'any').\n"
        "- Vérifie la conformité aux normes : " + standards + "\n"
        "- Si erreurs : Liste-les par ligne, explique, et propose un code corrigé complet.\n\n"
        "Code :\n```\n" + code + "\n```\n\n"
        'Réponds **uniquement** en JSON (sans ```json) :\n'
        '{\n'
        '  "errors": [\n'
        '    { "line": int, "description": str, "correction": str }\n'
        '  ],\n'
        '  "is_valid": bool,\n'
        '  "corrected_code": str\n'
        '}'
    ).strip()

    try:
        response = model.generate_content(prompt)
        cleaned = response.text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        data = json.loads(cleaned.strip())
        return data
    except json.JSONDecodeError as e:
        print(f"Erreur parsing JSON : {e}")
        return {
            "errors": [{"line": 0, "description": "Erreur analyse", "correction": ""}],
            "is_valid": False,
            "corrected_code": ""
        }
    except Exception as e:
        print(f"Erreur Gemini : {e}")
        return {
            "errors": [{"line": 0, "description": "Erreur IA", "correction": ""}],
            "is_valid": False,
            "corrected_code": ""
        }


def get_collaborators_emails():
    if not GITHUB_TOKEN:
        print("Pas de GITHUB_TOKEN → fallback sur ton email.")
        return [(COLLAB_NAME, COLLAB_EMAIL)]

    headers = {'Authorization': f'token {GITHUB_TOKEN}', 'Accept': 'application/vnd.github+json'}
    url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/collaborators"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur API : {e} → fallback sur ton email.")
        return [(COLLAB_NAME, COLLAB_EMAIL)]

    collab_list = []
    for user in resp.json():
        user_resp = requests.get(user['url'], headers=headers, timeout=10)
        if user_resp.status_code == 200:
            data = user_resp.json()
            name = data.get('name') or user['login']
            email = data.get('email') or f"{user['login']}@users.noreply.github.com"
            collab_list.append((name, email))
    return collab_list or [(COLLAB_NAME, COLLAB_EMAIL)]


def send_email(errors, corrected_code, file_paths, name, email):
    salutations = [f"Cher {name},", f"Bonjour {name},", f"Salut {name},"]
    intros = ["Merci pour votre contribution !", "Nous apprécions votre effort.", "Votre code est presque prêt."]
    explications = ["Quelques ajustements sont nécessaires.", "Des corrections mineures sont à faire.", "Petits points à rectifier."]
    fermetures = ["Cordialement,", "À bientôt,", "Bonne continuation,"]

    subject = f"Corrections pour gr4_project - {', '.join(file_paths[:2])}"
    body = f"""
{random.choice(salutations)}

{random.choice(intros)}

{random.choice(explications)} Voici les détails :

"""
    for err in errors:
        body += f"- Ligne {err['line']} : {err['description']}\n  → {err['correction']}\n\n"

    body += f"""
Code corrigé :

Merci de corriger et resoumettre !

{random.choice(fermetures)}
L'équipe gr4_project (IA)
"""

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, email, msg.as_string())
        server.quit()
        print(f"Email envoyé à {email} ({name}).")
    except smtplib.SMTPException as e:
        print(f"Erreur envoi à {email} ({name}) : {e}")


def send_emails_to_all(all_errors, corrected, files, local_mode):
    if local_mode:
        return
    for name, email in get_collaborators_emails():
        send_email(all_errors, corrected, files, name, email)


def write_pr_comment(all_errors, corrections):
    body = "# Erreurs détectées par l'IA\n\n"
    for err in all_errors:
        body += f"- Ligne {err['line']} : {err['description']}\n"
    body += "\n**Corrections :**\n"
    for file, code in corrections.items():
        body += f"### {file}\n```\n{code}\n```\n"

    os.makedirs('.github/scripts', exist_ok=True)
    with open('.github/scripts/error_comment.md', 'w', encoding='utf-8') as f:
        f.write(body)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--local', action='store_true')
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    changed = get_changed_files(args.files if args.local else None)
    if not changed:
        print("Aucun fichier à vérifier.")
        sys.exit(0)

    standards = load_standards()
    valid = True
    errors = []
    corrections = {}

    for file in changed:
        with open(file, 'r', encoding='utf-8') as f:
            code = f.read()

        result = analyze_with_gemini(code, standards, file)
        if not result.get('is_valid', True):
            valid = False
            errors.extend(result['errors'])
            corrections[file] = result['corrected_code']

    if not valid:
        corrected_str = '\n\n---\n\n'.join([f"{f}:\n{c}" for f, c in corrections.items()])
        send_emails_to_all(errors, corrected_str, changed, args.local)
        if not args.local:
            write_pr_comment(errors, corrections)
        print("Validation échouée.")
        sys.exit(1)
    else:
        print("Tout est bon !")
        sys.exit(0)


if __name__ == "__main__":
    main()
