import os
from typing import Optional

import magic
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from sqlalchemy.orm import Session
from settings import settings
from fastapi import Depends, APIRouter, UploadFile
from database import get_db
from schemat import attachment_dir
port = settings.port
serverEmail = settings.serverEmail
sender_email = settings.email
password = settings.password
dane = settings.dane

def send_mail(reciever: str, subject: str, content: str, file: Optional[UploadFile]):
    try:
        msg= EmailMessage()
        msg['Subject'] = subject
        msg['From'] = formataddr((dane, sender_email))
        msg['To'] = reciever
        msg.set_content(content)


        save_path = os.path.join(attachment_dir, file.filename)
        if file:
            with open(r'C:\Users\eheex\PycharmProjects\AutoEmail\funkcje\CV Kacper Prusik 2025 Internship.pdf','rb') as file:
                mime_type = magic.from_file(r"C:\Users\eheex\PycharmProjects\AutoEmail\funkcje\CV Kacper Prusik 2025 Internship.pdf", mime=True)
                maintype, subtype = mime_type.split('/')
                file_data=file.read()
                file_name='CV Kacper Prusik 2025 Internship'
                msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)

        with smtplib.SMTP(serverEmail, port) as server:
        #with smtplib.SMTP('localhost', 1025) as server:
            server.starttls()
            server.login(sender_email, password)
            #server.sendmail(sender_email, reciever, msg.as_string())
            server.send_message(msg)
            print(f"Mail wysłany na {reciever}")
    except Exception as e:
        print(f"❌ Błąd podczas wysyłania na {reciever}: {e}")
        print(repr(e))