import os
import smtplib
from email.message import EmailMessage
from typing import Optional

SMTP_SERVER = os.getenv("SMTP_SERVER")
try:
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
except ValueError:
    SMTP_PORT = 587  # Fallback to default if invalid

SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_email(to_email: str, subject: str, body: str, cc: Optional[str] = None, html: Optional[str] = None) -> None:
    if not all([SMTP_SERVER, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL]):
        raise RuntimeError("SMTP not configured in environment variables")
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    if cc:
        msg["Cc"] = cc
    msg["Subject"] = subject
    msg.set_content(body)
    if html:
        msg.add_alternative(html, subtype="html")  # For richer formatting

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASSWORD)
        s.send_message(msg)