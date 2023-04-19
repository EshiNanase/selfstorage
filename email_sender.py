import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.image import MIMEImage  # Изображения

from dotenv import load_dotenv


def send_email(msg_body: str, subject: str, receiver: str):
    load_dotenv()
    smtpobj = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    smtpobj.login(os.environ['EMAIL_LOGIN'], os.environ['EMAIL_PASSWORD'])
    smtpobj.set_debuglevel(True)

    msg = MIMEMultipart()
    msg['From'] = os.environ['EMAIL_LOGIN']
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(msg_body, 'plain'))

    smtpobj.send_message(msg)
    smtpobj.quit()
