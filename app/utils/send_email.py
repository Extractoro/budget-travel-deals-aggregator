import os

from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail
from dotenv import load_dotenv
from pydantic import EmailStr

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM'),
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_FROM_NAME=os.getenv('MAIL_FROM_NAME'),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)


async def send_email_alert(to_email: EmailStr, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=body,
        subtype=MessageType.plain
    )

    fm = FastMail(conf)
    await fm.send_message(message)
