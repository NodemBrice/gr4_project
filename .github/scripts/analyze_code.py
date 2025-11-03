"""Analyseur de code IA avec verification stricte des standards."""
import argparse
import json
import os
import smtplib
import subprocess
import sys
from email.mime.text import MIMEText
from typing import Any, Dict, List, Tuple

import google.generativeai as genai # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

load_dotenv()

# Configuration
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))  # type: ignore[attr-defined]
model = genai.GenerativeModel('gemini-2.5-flash')  # type: ignore[attr-defined]
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


def get_files() -> List[str]:

    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', '--diff-filter=AM'],
        capture_output=True, text=True, check=False
    )
    return [f for f in result.stdout.split('\n')
            if f.strip() and f.endswith(('.py', '.html', '.js', '.jsx'))]


def run_linter(file: str) -> Tuple[bool, List[str]]:
    """Execute le linter approprie selon le fichier."""
    ext = file.split('.')[-1]
    errors: List[str] = []

    try:
        if ext == 'py':
            # Pylint
            r = subprocess.run(['pylint', file, '--rcfile=.pylintrc',
                              '--output-format=json'],
                              capture_output=True, text=True, check=False)
            if r.returncode != 0 and r.stdout.strip():
                try:
                    pylint_data = json.loads(r.stdout)
                    for e in pylint_data:
                        errors.append(
                            f"Ligne {e['line']}: {e['message']} [{e['symbol']}]"
                        )
                except json.JSONDecodeError:
                    pass

            # MyPy
            r = subprocess.run(['mypy', file, '--strict'],
                             capture_output=True, text=True, check=False)
            if r.returncode != 0:
                errors.extend([f"MyPy: {line}" for line in r.stdout.split('\n')
                             if line.strip() and ':' in line])

        elif ext in ['js', 'jsx']:
            r = subprocess.run(['npx', 'eslint', file,
                              '--config=.eslintrc.json', '--format=json'],
                              capture_output=True, text=True, check=False)
            if r.returncode != 0 and r.stdout.strip():
                try:
                    eslint_data = json.loads(r.stdout)
                    for f_result in eslint_data:
                        for e in f_result.get('messages', []):
                            errors.append(
                                f"Ligne {e['line']}: {e['message']} "
                                f"({e.get('ruleId', '')})"
                            )
                except json.JSONDecodeError:
                    pass

        elif ext in ['html', 'htm']:
            r = subprocess.run(['npx', 'htmlhint', file,
                              '--config=.htmlhintrc'],
                              capture_output=True, text=True, check=False)
            if r.returncode != 0:
                errors.extend([line for line in r.stdout.split('\n')
                             if 'line' in line.lower()])

    except FileNotFoundError as e:
        errors.append(f"Linter non installe: {e}")

    return len(errors) == 0, errors


def analyze_with_ai(file: str, code: str,
                   linter_errors: List[str]) -> Dict[str, Any]:
    """Analyse le code avec Gemini et genere un message personnalise."""
    lang = file.split('.')[-1].upper()

    linter_ctx = "\n".join(f"- {e}" for e in linter_errors) \
                 if linter_errors else "Aucune"

    prompt = f"""Tu es un expert {lang}. Analyse ce code du fichier {file}.

ERREURS LINTERS:
{linter_ctx}

CODE:
```{lang.lower()}
{code}
```

Retourne un JSON (sans markdown):
{{
  "is_valid": true/false,
  "errors": [{{"line": int, "description": str, "fix": str}}],
  "corrected_code": "code corrige si is_valid=false",
  "email_message": {{
    "subject": "sujet email court et precis",
    "greeting": "salutation personnalisee unique",
    "intro": "phrase d'introduction unique",
    "conclusion": "phrase de conclusion unique et encourageante"
  }}
}}

IMPORTANT: Genere un message EMAIL unique et different a chaque fois et
Reponds **uniquement** avec un objet JSON valide, sans aucun texte avant ou après.
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Nettoyage
        for marker in ['```json', '```']:
            text = text.replace(marker, '')

        data: Dict[str, Any] = json.loads(text.strip())

        # Force invalide si erreurs linters
        if linter_errors:
            data['is_valid'] = False

        return data

    except Exception as e:  # pylint: disable=broad-exception-caught
        return {
            "is_valid": False,
            "errors": [{"line": 0, "description": f"Erreur IA: {e}",
                       "fix": "Reessaye"}],
            "corrected_code": code,
            "email_message": {
                "subject": "Erreur analyse",
                "greeting": "Bonjour,",
                "intro": "L'analyse a echoue.",
                "conclusion": "Reessaye plus tard."
            }
        }


def send_email(to_email: str, to_name: str, # pylint: disable=unused-argument
              all_errors: Dict[str, Dict[str, Any]],
              email_msg: Dict[str, str]) -> None:
    """Envoie l'email avec le message genere par Gemini."""
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        print("Config email manquante")
        return

    body = f"""{email_msg['greeting']}

{email_msg['intro']}

{'='*70}
ERREURS DETECTEES
{'='*70}

"""

    for file, data in all_errors.items():
        body += f"\nFichier: {file}\n{'-'*70}\n"

        if data['linter_errors']:
            body += "\nERREURS LINTERS:\n"
            for err in data['linter_errors']:
                body += f"  - {err}\n"

        if data['ai_errors']:
            body += "\nANALYSE IA:\n"
            for err in data['ai_errors']:
                body += f"  - Ligne {err['line']}: {err['description']}\n"
                body += f"    Solution: {err['fix']}\n"

        if data['corrected_code']:
            lang = file.split('.')[-1]
            code_preview = data['corrected_code'][:800] + "..." \
                          if len(data['corrected_code']) > 800 \
                          else data['corrected_code']
            body += f"\nCODE CORRIGE:\n```{lang}\n{code_preview}\n```\n"

    body += f"\n{'='*70}\n{email_msg['conclusion']}\n"

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = EMAIL_SENDER
    msg['To'] = to_email
    msg['Subject'] = email_msg['subject']

    try:
        with smtplib.SMTP(os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
                         int(os.getenv('SMTP_PORT', '587'))) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        print(f"Email envoye a {to_email}")
    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"Erreur email: {e}")


def get_user_info() -> Tuple[str, str]:
    """Recupere nom et email de l'utilisateur Git."""
    try:
        name = subprocess.run(['git', 'config', 'user.name'],
                            capture_output=True, text=True,
                            check=False).stdout.strip()
        email = subprocess.run(['git', 'config', 'user.email'],
                             capture_output=True, text=True,
                             check=False).stdout.strip()
        return name or "Dev", email or "dev@example.com"
    except Exception:  # pylint: disable=broad-exception-caught
        return "Dev", "dev@example.com"


def main() -> None:
    """Fonction principale."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--local', action='store_true')
    args = parser.parse_args()

    print("\n" + "="*70)
    print("ANALYSEUR CODE IA - Verification Standards")
    print("="*70 + "\n")

    files = get_files()
    if not files:
        print("Aucun fichier a analyser")
        sys.exit(0)

    print(f"{len(files)} fichier(s):")
    for file_path in files:
        print(f"   - {file_path}")

    all_errors: Dict[str, Dict[str, Any]] = {}
    email_message: Dict[str, str] = {}

    for file_path in files:
        print(f"\n{'='*70}\n{file_path}\n{'='*70}")

        try:
            with open(file_path, 'r', encoding='utf-8') as file_handle:
                code = file_handle.read()
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"Erreur lecture: {e}")
            continue

        # Linters
        linter_ok, linter_errors = run_linter(file_path)
        status = "OK" if linter_ok else f"{len(linter_errors)} erreur(s)"
        print(f"Linters: {status}")

        # IA
        print("Analyse IA...")
        ai_result = analyze_with_ai(file_path, code, linter_errors)

        is_valid = ai_result.get('is_valid', True) and linter_ok

        if not is_valid:
            all_errors[file_path] = {
                'linter_errors': linter_errors,
                'ai_errors': ai_result.get('errors', []),
                'corrected_code': ai_result.get('corrected_code', '')
            }
            email_message = ai_result.get('email_message', {})
            print("REJETE")
        else:
            print("VALIDE")

    print("\n" + "="*70)

    if all_errors:
        print(f"COMMIT REJETE - {len(all_errors)} fichier(s) en erreur\n")

        name, email = get_user_info()

        if not args.local and email_message:
            send_email(email, name, all_errors, email_message)

        print("Corrige les erreurs et recommite\n")
        sys.exit(1)

    print("COMMIT VALIDE - Code conforme\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
