
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from sqlalchemy.orm import Session
from settings import settings
from fastapi import Depends, APIRouter
from database import get_db

port = settings.port
serverEmail = settings.serverEmail
sender_email = settings.email
password = settings.password
dane = settings.dane

def send_mail(reciever: str, subject: str, content: str):
    try:
        msg= EmailMessage()
        msg['Subject'] = subject
        msg['From'] = formataddr((dane, sender_email))
        msg['To'] = reciever
        msg.set_content(content)

        with smtplib.SMTP(serverEmail, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, reciever, msg.as_string())
            print(f"Mail wysłany na {reciever}")
    except Exception as e:
        print(f"❌ Błąd podczas wysyłania na {reciever}: {e}")