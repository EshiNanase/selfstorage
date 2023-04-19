import smtplib
import sys
from datetime import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# from email.mime.image import MIMEImage  # Изображения
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db.models import QuerySet

from personal_account.models import Client


def send_email(msg_body: str, subject: str, receivers: QuerySet[Client]):
    email_validator = EmailValidator()

    sender_email = settings.EMAIL_NOTIFIER_LOGIN
    sender_password = settings.EMAIL_NOTIFIER_PASSWORD
    smtp_server = settings.EMAIL_NOTIFIER_SMTP_SERVER
    smtp_server_port = settings.EMAIL_NOTIFIER_SMTP_SERVER_PORT

    smtpobj = smtplib.SMTP_SSL(smtp_server, smtp_server_port)
    smtpobj.login(sender_email, sender_password)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = subject

    for receiver in receivers:
        receiver_email = receiver.email
        try:
            email_validator(receiver_email)
        except ValidationError:
            continue

        msg['To'] = receiver_email
        msg.attach(MIMEText(msg_body, 'plain'))
        smtpobj.send_message(msg)
        time.sleep = 5

    smtpobj.quit()
