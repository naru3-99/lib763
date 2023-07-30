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
    ) -> None:
        """
        SSHOperatorクラスのコンストラクター。

        Args:
            username (str): SSH接続に使用するユーザー名。
            hostname (str): SSH接続に使用するホスト名。
            password (str): SSH接続に使用するパスワード。
            key_path (str, optional): SSH接続に使用する秘密鍵のパス。デフォルトはNone。
            port (int, optional): SSH接続に使用するポート番号。デフォルトは22。
        """
        self._username: str = username
        self._hostname: str = hostname
        self._password: str = password
        self._key_path: str = key_path
        self._port: int = port
        self._client: paramiko.SSHClient = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect_ssh(self) -> bool:
        """
        SSH接続を確立するメソッド。

        Returns:
            bool: 成功するとTrue、失敗するとFalse
        """
        try:
            self._client.connect(
                self._hostname,
                username=self._username,
                password=self._password,
                key_filename=self._key_path,
                port=self._port
            )
            return True
        except:
            return False

    def execute(self, command: str) -> tuple[int, str, str]:
        """
        コマンドを実行するメソッド。

        Args:
            command (str): 実行するコマンド。

        Returns:
            tuple[int, str, str]: コマンドの実行結果。
        """
        if not self.get_ssh_state():
            raise SSHConnectionError("SSH接続が有効ではありません。")
        _, stdout, stderr = self._client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        return exit_status, stdout.read().decode("utf-8"), stderr.read().decode("utf-8")

    def execute_sudo(self, command: str) -> tuple[int, str, str]:
        """
        sudoコマンドを実行するメソッド。

        Args:
            command (str): 実行するsudoコマンド。

        Returns:
            tuple[int, str, str]: コマンドの実行結果。
        """
        return self.execute(f"echo {self._password} | sudo -S {command}")

    def send_file(self, local_path: str, remote_path: str) -> bool:
        """
        ファイルをリモートホストに送信するメソッド。

        Args:
            local_path (str): 送信するファイルのローカルパス。
            remote_path (str): 送信するファイルのリモートパス。

        Returns:
            bool: ファイルの送信が成功した場合はTrue、失敗した場合はFalse。
        """
        if not self.get_ssh_state():
            raise SSHConnectionError("SSH接続が有効ではありません。")
        try:
            with SCPClient(self._client.get_transport()) as scp:
                scp.put(local_path, remote_path)
            return True
        except:
            return False

    def get_ssh_state(self) -> bool:
        """
        SSH接続の状態を取得するメソッド。

        Returns:
            bool: SSH接続が有効な場合はTrue、無効な場合はFalse。
        """
        if self._client.get_transport() is None:
            return False
        return self._client.get_transport().is_active()

    def exit(self) -> None:
        """
        SSH接続を終了するメソッド。
        """
        self._client.close()


class SSHConnectionError(Exception):
    """
    SSH接続エラーを処理するためのカスタム例外クラス。
    """

    pass
