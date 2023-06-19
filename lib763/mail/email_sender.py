import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class email_sender:
    def __init__(
        self,
        sender: str,
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        username: str = None,
        password: str = None,
    ):
        self.sender = sender
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send(self, recipients: list, subject: str, body: str):
        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["Subject"] = subject
        msg.attach(MIMEText(body))

        smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
        smtp.starttls()
        if self.username and self.password:
            smtp.login(self.username, self.password)

        for recipient in recipients:
            msg["To"] = recipient
            smtp.sendmail(self.sender, recipient, msg.as_string())
        smtp.quit()
