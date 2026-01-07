# app/services/email_service.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


def enviar_correo( asunto: str, cuerpo: str) -> None:
    """Envía un correo por SMTP usando Gmail (STARTTLS)."""

# Seguridad: flag general
    if not settings.EMAIL_ENABLED:
        return

    # Validación SMTP
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        raise RuntimeError("SMTP_USER/SMTP_PASSWORD no configurados en .env")

    # Destinatario fijo (CLAVE)
    destino = settings.EMAIL_DEFAULT_TO.strip()
    if not destino or "@" not in destino:
        raise RuntimeError(f"Destino de correo inválido: {destino}")

    # Emisor
    mail_from = settings.SMTP_FROM or settings.SMTP_USER

    # Construcción del mensaje
    msg = MIMEMultipart()
    msg["From"] = mail_from
    msg["To"] = destino
    msg["Subject"] = asunto
    msg.attach(MIMEText(cuerpo, "plain", "utf-8"))

    # Envío SMTP
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)