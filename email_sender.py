import smtplib
from datetime import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.image import MIMEImage  # Изображения
from typing import Iterable

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


def send_email(msg_body: str, subject: str, receivers: Iterable[str]) -> set[str]:
    """
    Рассылка писем по списку получателей
    :param msg_body: Текст письма
    :param subject: Тема письма
    :param receivers: Список почтовых ящиков для рассылки
    :return: Список почтовых ящиков, по которым удалась рассылка
    """
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

    success_sent = set()
    for receiver in receivers:
        try:
            email_validator(receiver)
        except ValidationError:
            print(f'Некорректный email: {receiver}')
            continue

        msg['To'] = receiver
        msg.attach(MIMEText(msg_body, 'plain'))
        try:
            smtpobj.send_message(msg)
        except smtplib.SMTPResponseException as ex:
            print(ex)
            continue
        success_sent.add(receiver)
    smtpobj.quit()

    return success_sent
