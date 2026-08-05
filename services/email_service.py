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

enviar_email("fernando.alves@enel.com", "TESTE DE ENVIO", "relatorio enviado com sucesso!", anexo=r"C:\Users\BR0459067248\Documents\GitHub\DASH_MEDIDORES\base\consulta_instalacoes.xlsx")