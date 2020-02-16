# Import smtplib for our actual email sending function
import smtplib

# Helper email modules
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time

class SMTPSender(object):
    def __init__(self, email, password, subject=""):
        self.sender = email
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(email, password)
        self.subject = subject

    def logout(self):
        self.server.quit()

    def send_message(self, message, email):
        time.sleep(1) # to keep gmail happy

        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = email
        msg['Subject'] = self.subject

        body = message
        msg.attach(MIMEText(body, 'html'))
        text = msg.as_string()

        self.server.sendmail(email, self.sender, text)
