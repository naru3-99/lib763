import paramiko
from scp import SCPClient


class SSHOperator:
    def __init__(
        self,
        username: str,
        hostname: str,
        password: str,
        key_path: str = None,
        port: int = 22,
    ):
        """
        初期化処理
        :param username: SSH接続のユーザー名
        :param hostname: SSH接続のホスト名
        :param password: SSH接続のパスワード
        :param key_path: SSHの秘密鍵のファイルパス
        :param port: SSH接続のポート番号 (デフォルトは22)
        """
        self.username = username
        self.hostname = hostname
        self.password = password
        self.key_path = key_path
        self.port = port
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        ) 
        self._init_ssh()

    def _init_ssh(self):
        """
        SSH接続を初期化する。
        """
        self.client.connect(
            self.hostname,
            username=self.username,
            password=self.password,
            key_filename=self.key_path,
            port=self.port,
        )

    def execute(self, command: str) -> str:
        """
        コマンドを実行する。
        :param command: 実行するコマンド
        :return: コマンドの出力
        """
        if not self.client.get_transport().is_active():
            raise SSHConnectionError("SSH接続が有効ではありません。")
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode("utf-8")

    def send_file(self, local_path: str, remote_path: str):
        """
        ファイルをリモートシステムに送信する。
        :param local_path: ローカルのファイルパス
        :param remote_path: リモートのファイルパス
        """
        if not self.client.get_transport().is_active():
            raise SSHConnectionError("SSH接続が有効ではありません。")
        with SCPClient(self.client.get_transport()) as scp:
            scp.put(local_path, remote_path)

    def exit(self):
        """
        SSH接続を閉じる。
        """
        self.client.close()


class SSHConnectionError(Exception):
    """
    SSH接続エラーを処理するためのカスタム例外クラス。
    """

    pass
