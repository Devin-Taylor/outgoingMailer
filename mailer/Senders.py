import email.utils
import logging
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SMTPSender(object):
    def __init__(self, email: str, password: str, subject: str = "", display_email: str = "", display_name: str = ""):
        logging.info("Instantiating SMTP server")
        self.sender = email
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(email, password)
        self.subject = subject
        self.display_email = display_email
        self.display_name = display_name
        logging.info("SMTP server instantiated")

    def logout(self):
        logging.info("Logging out of SMTP server")
        self.server.quit()

    def send_message(self, message: str, email_addr: str):
        time.sleep(1) # to keep gmail happy, breaks if you send ~80 emails/minute so just limit it to at best 60

        msg = MIMEMultipart()
        if self.display_name:
            if self.display_email:
                msg['From'] = email.utils.formataddr(
                                (self.display_name, self.display_email))
            else:
                msg['From'] = email.utils.formataddr(
                                (self.display_name, self.sender))
        else:
            msg['From'] = self.sender
        msg['To'] = email_addr
        msg['Subject'] = self.subject

        body = message
        msg.attach(MIMEText(body, 'html'))
        text = msg.as_string()

        self.server.sendmail(self.sender, email_addr, text)
