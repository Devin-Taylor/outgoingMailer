# Import smtplib for our actual email sending function
import logging
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
# Helper email modules
from email.mime.text import MIMEText


class SMTPSender(object):
    def __init__(self, email, password, subject=""):
        logging.info("Instantiating SMTP server")
        self.sender = email
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(email, password)
        self.subject = subject
        logging.info("SMTP server instantiated")

    def logout(self):
        logging.info("Logging out of SMTP server")
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
