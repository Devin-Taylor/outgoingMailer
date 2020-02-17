import logging
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SMTPSender(object):
    def __init__(self, email: str, password: str, subject: str = ""):
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

    def send_message(self, message: str, email: str):
        time.sleep(1) # to keep gmail happy, breaks if you send ~80 emails/minute so just limit it to at best 60

        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = email
        msg['Subject'] = self.subject

        body = message
        msg.attach(MIMEText(body, 'html'))
        text = msg.as_string()

        self.server.sendmail(email, self.sender, text)
