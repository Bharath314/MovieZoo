import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(
        address, 
        subject, 
        message, 
        attachment = None, 
        images = None, 
        filename = None, 
        subtype = None
    ):

    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "support@moviezoo.com"
    SENDER_PASSWORD = ""

    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = address
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))

    if attachment:
        part = MIMEApplication(attachment.read(), _subtype=subtype)
        part.add_header("Content-Disposition", "attachment", filename)
        msg.attach(part)
    
    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    print("hey")
    s.quit()
