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
        SSHOperatorクラスの初期化メソッド。

        Args:
            username (str): SSH接続のユーザー名。
            hostname (str): SSH接続のホスト名。
            password (str): SSH接続のパスワード。
            key_path (str, optional): SSHの秘密鍵のファイルパス。デフォルトはNone。
            port (int, optional): SSH接続のポート番号。デフォルトは22。

        Raises:
            SSHConnectionError: SSH接続が失敗した場合に発生。
        """
        self._username = username
        self._hostname = hostname
        self._password = password
        self._key_path = key_path
        self._port = port
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._init_ssh()

    def _init_ssh(self):
        """
        SSH接続を初期化するプライベートメソッド。

        Raises:
            SSHConnectionError: SSH接続が失敗した場合に発生。
        """
        try:
            self._client.connect(
                self._hostname,
                username=self._username,
                password=self._password,
                key_filename=self._key_path,
                port=self._port,
            )
        except Exception as e:
            raise SSHConnectionError("SSH connection failed.") from e

    def execute(self, command: str) -> str:
        """
        SSH接続を通じてリモートコマンドを実行する。

        Args:
            command (str): 実行するコマンド。

        Returns:
            str: コマンドの実行結果。

        Raises:
            SSHConnectionError: SSH接続が有効でない場合に発生。
        """
        if not self.get_ssh_state():
            raise SSHConnectionError("SSH接続が有効ではありません。")
        stdin, stdout, stderr = self._client.exec_command(command)
        return stdout.read().decode("utf-8")

    def send_file(self, local_path: str, remote_path: str):
        """
        ファイルをリモートシステムに送信する。

        Args:
            local_path (str): ローカルのファイルパス。
            remote_path (str): リモートのファイルパス。

        Raises:
            SSHConnectionError: SSH接続が有効でない場合に発生。
        """
        if not self.get_ssh_state():
            raise SSHConnectionError("SSH接続が有効ではありません。")
        with SCPClient(self._client.get_transport()) as scp:
            scp.put(local_path, remote_path)

    def get_ssh_state(self) -> bool:
        """
        現在のSSH接続の状態を確認します。

        Returns:
            bool: SSH接続が有効な場合はTrue、そうでない場合はFalse。
        """
        return self._client.get_transport().is_active()

    def exit(self):
        """
        SSH接続を閉じる。
        """
        self._client.close()


class SSHConnectionError(Exception):
    """
    SSH接続エラーを処理するためのカスタム例外クラス。
    """
    pass
