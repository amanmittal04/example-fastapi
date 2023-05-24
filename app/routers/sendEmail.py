from typing import List
from fastapi import APIRouter, Response
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel
from app.config import settings
# from dotenv import dotenv_values

# credentials = dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME=settings.email,
    MAIL_PASSWORD=settings.password,
    MAIL_FROM=settings.email,
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_email(email: str, content: str, subject: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=content,
        subtype=MessageType.plain)
    fm = FastMail(conf)
    await fm.send_message(message)
    return Response(status_code=200)
