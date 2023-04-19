import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.image import MIMEImage  # Изображения

from dotenv import load_dotenv


def send_email(msg_body: str, subject: str, receiver: str):
    load_dotenv()
    smtpobj = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    smtpobj.login(os.environ['LOGIN'], os.environ['PASSWORD'])
    smtpobj.set_debuglevel(True)

    msg = MIMEMultipart()
    msg['From'] = os.environ['LOGIN']
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(msg_body, 'plain'))

    smtpobj.send_message(msg)
    smtpobj.quit()


if __name__ == '__main__':
    send_email(
        msg_body='Привет',
        subject='Привет',
        receiver='ns-tonic@yandex.ru'
    )