import json
import os
import argparse
import requests
import pandas as pd

# Reuse from backend if possible, but for script, duplicate or import
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

def ai_rephrase(profile, report_summary):
    prompt = f"""
Tu es une IA qui reformule un rapport technique pour un développeur.
Profil du destinataire: {profile}
Rapport: {report_summary}

Formule un message poli, clair, adapté au profil (débutant/pro/intermédiaire).
Inclue suggestions précises et liens utiles si possible.
"""
    headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
    body = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 600,
    }
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body, timeout=30)
        r.raise_for_status()
        data = r.json()
        text = data["choices"][0]["message"]["content"]
        return text
    except Exception as e:
        return f"Error with AI: {str(e)}\nRaw report: {report_summary}"

def send_mail(to_addr, subject, body):
    # Ideally, import backend.email_sender and use send_email
    # For now, duplicate
    import smtplib
    from email.message import EmailMessage
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_addr
    if ADMIN_EMAIL:
        msg["Cc"] = ADMIN_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASSWORD)
        s.send_message(msg)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="report.json")
    args = parser.parse_args()

    with open(args.report, "r", encoding="utf-8") as f:
        report = json.load(f)

    if not report.get("failed"):
        print("No failures - nothing to send.")
        return

    author = report.get("author", "unknown")
    author_name, author_email = author.split("<") if "<" in author else (author, None)
    author_email = author_email.strip(">").strip() if author_email else "unknown"

    # Load profiles
    profile = {"level": "intermediate", "tone": "neutral"}
    if os.path.exists("profiles.xlsx"):
        df = pd.read_excel("profiles.xlsx")
        found = df[df["email"].str.lower() == author_email.lower()]
        if not found.empty:
            row = found.iloc[0]
            profile = {"level": row.get("level", "intermediate"), "tone": row.get("tone", "neutral")}

    # Build summary
    summary = "\n\n".join([f"{c['name']} output:\n{c['output']}" for c in report.get("checks", [])])
    ai_text = ai_rephrase(profile, summary)

    # Determine to_addr
    to_addr = author_email if author_email != "unknown" else ADMIN_EMAIL
    if found.empty and os.path.exists("profiles.xlsx"):
        to_addr = ADMIN_EMAIL  # Fallback if no match

    subject = "Votre code n’a pas passé les checks automatiques"
    body = f"Bonjour,\n\nLe pipeline CI a détecté des problèmes sur votre push.\n\nAI reformulation:\n\n{ai_text}\n\n---\nRapport brut:\n{summary}"

    send_mail(to_addr, subject, body)
    print("Mail sent to", to_addr)

if __name__ == "__main__":
    main()