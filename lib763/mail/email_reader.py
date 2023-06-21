import imaplib
import base64
import datetime
import email
from email.header import decode_header


class email_reader:
    def __init__(
        self, username: str, password: str, imap_address="imap.gmail.com", search_days=7
    ) -> None:
        """
        コンストラクタ
        @param:
            username: (str) ユーザー名
            password: (str) パスワード
            imap_address: (str) IMAPサーバーアドレス
            search_days: (int) 検索対象とする日数
        """
        self.username = username
        self.password = password
        self.imap_address = imap_address
        self.search_days = search_days
        self.imap = None

    def __init_imap(self) -> None:
        """
        IMAP接続を初期化する
        """
        self.imap = imaplib.IMAP4_SSL(self.imap_address)
        self.imap.login(self.username, self.password)
        self.imap.select("inbox")

    def __search_mail(self, criteria: str) -> list:
        """
        指定されたクリテリアに基づいてメールを検索する
        @param:
            criteria: (str) 検索条件
        @return:
            (list[msg]) メールのリスト
        """
        status, messages = self.imap.search(None, criteria)
        messages = messages[0].split(b" ")
        msg_ls = []
        one_week_ago = datetime.datetime.now() - datetime.timedelta(
            days=self.search_days
        )

        for email_uid in messages[::-1]:
            res, msg = self.imap.fetch(email_uid, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    date_obj = self.get_datetime(msg)
                    if date_obj < one_week_ago:
                        return msg_ls
                    msg_ls.append(msg)
        return msg_ls

    def get_msgs_by(self, criteria: str) -> list:
        """
        指定されたクリテリアに基づいてメールのリストを取得する
        @param:
            criteria: (str) 検索条件
        @return:
            (list[msg]) メールのリスト
        """
        self.__init_imap()
        return self.__search_mail(criteria)

    def get_datetime(self, msg) -> datetime:
        """
        メールが送信された日時のdatetimeオブジェクトを取得する
        @param:
            msg: メールオブジェクト
        @return:
            (datetime) 送信日時のdatetimeオブジェクト
        """
        date_str = msg["Date"]
        date_ls = date_str.split(",")[1].split(" ")[1:4]
        date_obj = datetime.datetime.strptime(
            "-".join(date_ls[::-1])
            + "-"
            + date_str.split(",")[1].split(" ")[4].replace(":", "-"),
            "%Y-%b-%d-%H-%M-%S",
        )
        return date_obj

    def get_time_stamp(self, msg) -> str:
        """
        メールが送信された日時の文字列を取得する
        @param:
            msg: メールオブジェクト
        @return:
            (str) 送信日時の文字列
        """
        date_obj = self.get_datetime(msg)
        return date_obj.strftime("%Y-%m-%d-%H-%M-%S")

    def get_body_str(self, msg) -> str | None:
        """
        メールの本文を取得する
        @param:
            msg: メールオブジェクト
        @return:
            (str) メールの本文
        """
        if msg.is_multipart() is False:
            payload = msg.get_payload(decode=True)
            charset = msg.get_content_charset()
            if charset is not None:
                return payload.decode(charset, "ignore")
            return None

        ret_str = ""
        for part in msg.walk():
            payload = part.get_payload(decode=True)
            if payload is None:
                continue

            charset = part.get_content_charset()
            if charset is not None:
                payload = payload.decode(charset, "ignore")
                ret_str += payload
        return ret_str if (len(ret_str) != 0) else None

    def get_subject(self, msg) -> str:
        """
        メールのタイトルを取得する
        @param:
            msg: メールオブジェクト
        @return:
            (str) メールのタイトル
        """
        subject = decode_header(msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()
        return subject

    def save_attachment(self, path: str, msg) -> str | None:
        """
        添付ファイルを保存する
        @param:
            path: (str) 保存先のパス
            msg: メールオブジェクト
        @return:
            (str) 保存したファイルのパス
        """
        for part in msg.walk():
            file_name = part.get_filename()
            if not file_name:
                continue
            fns = file_name.split("?")
            output_file_name = self.get_time_stamp(msg) + base64.b64decode(
                fns[-2]
            ).decode(fns[1])
            with open(f"{path}/{output_file_name}", "wb") as f:
                f.write(part.get_payload(decode=True))
            return output_file_name
        return None

    def exit(self):
        """
        IMAP接続を終了する
        """
        self.imap.close()
        self.imap.logout()
