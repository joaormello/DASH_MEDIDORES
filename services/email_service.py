from pathlib import Path

import win32com.client as win32


def enviar_email(
    destinatario: str,
    assunto: str,
    corpo: str,
    anexo: Path | str | None = None,
) -> None:

    outlook = win32.Dispatch("Outlook.Application")
    email = outlook.CreateItem(0)

    email.To = destinatario
    email.Subject = assunto
    email.Body = corpo

    if anexo is not None:
        email.Attachments.Add(str(anexo))

    email.Display()      # Para revisar antes de enviar
    email.Send()       # Descomente para enviar automaticamente