import win32com.client as win32 

def enviar_email(destinatario:str, assunto:str, corpo:str, anexo=None):
    outlook = win32.Dispatch("Outlook.Application")
    email = outlook.CreateItem(0)

    email.To = destinatario
    email.Subject = assunto
    email.Body = corpo

    if anexo:
        email.Attachments.Add(anexo)

    email.Display()

