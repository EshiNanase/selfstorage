import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.image import MIMEImage  # Изображения
from typing import Iterable

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


def send_email_by_receivers(msg_body: str, subject: str, receivers: Iterable[str]) -> set[str]:
    """
    Рассылка писем по списку получателей
    :param msg_body: Текст письма
    :param subject: Тема письма
    :param receivers: Список почтовых ящиков для рассылки
    :return: Список почтовых ящиков, по которым удалась рассылка
    """
    sender_email = settings.EMAIL_NOTIFIER_LOGIN
    sender_password = settings.EMAIL_NOTIFIER_PASSWORD
    smtp_server = settings.EMAIL_NOTIFIER_SMTP_SERVER
    smtp_server_port = settings.EMAIL_NOTIFIER_SMTP_SERVER_PORT

    success_sent = set()
    smtpobj = smtplib.SMTP_SSL(smtp_server, smtp_server_port)
    smtpobj.login(sender_email, sender_password)
    for receiver in receivers:
        if send_email(msg_body, subject, receiver, user_defined_smtpobj=smtpobj):
            success_sent.add(receiver)
    smtpobj.quit()
    return success_sent


def send_email(msg_body: str, subject: str, receiver: str, user_defined_smtpobj: smtplib.SMTP_SSL = None):
    email_validator = EmailValidator()

    sender_email = settings.EMAIL_NOTIFIER_LOGIN
    sender_password = settings.EMAIL_NOTIFIER_PASSWORD
    smtp_server = settings.EMAIL_NOTIFIER_SMTP_SERVER
    smtp_server_port = settings.EMAIL_NOTIFIER_SMTP_SERVER_PORT

    if not user_defined_smtpobj:
        smtpobj = smtplib.SMTP_SSL(smtp_server, smtp_server_port)
        smtpobj.login(sender_email, sender_password)
    else:
        smtpobj = user_defined_smtpobj

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = subject

    try:
        email_validator(receiver)
    except ValidationError:
        print(f'Некорректный email: {receiver}')
        if not user_defined_smtpobj:
            smtpobj.quit()
        return

    msg['To'] = receiver
    msg.attach(MIMEText(msg_body, 'plain'))
    try:
        smtpobj.send_message(msg)
    except smtplib.SMTPResponseException as ex:
        print(ex)
        if not user_defined_smtpobj:
            smtpobj.quit()
        return

    if not user_defined_smtpobj:
        smtpobj.quit()

    return True
