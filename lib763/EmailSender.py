import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(
        self,
        sender: str,
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        username: str = None,
        password: str = None,
    ):
        """
        コンストラクタ
        @param:
            sender: (str) 送信元メールアドレス
            smtp_server: (str) SMTPサーバーのアドレス
            smtp_port: (int) SMTPポート番号
            username: (str) SMTP認証に使用するユーザー名
            password: (str) SMTP認証に使用するパスワード
        """
        self.sender = sender
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send(self, recipients: list, subject: str, body: str):
        """
        メールを送信する
        @param:
            recipients: (list) 受信者のメールアドレスのリスト
            subject: (str) メールの件名
            body: (str) メールの本文
        """
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
