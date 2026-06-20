import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


def enviar_correo(
    destinatario: str,
    asunto: str,
    cuerpo: str,
    adjunto_nombre: str,
    adjunto_contenido: bytes,
) -> None:
    mensaje = MIMEMultipart()
    mensaje["From"] = settings.smtp_from
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(cuerpo, "plain"))

    adjunto = MIMEApplication(adjunto_contenido, Name=adjunto_nombre)
    adjunto["Content-Disposition"] = f'attachment; filename="{adjunto_nombre}"'
    mensaje.attach(adjunto)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as servidor:
        servidor.starttls()
        servidor.login(settings.smtp_user, settings.smtp_password)
        servidor.sendmail(settings.smtp_from, destinatario, mensaje.as_string())
