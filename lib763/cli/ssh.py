from lib763.cli.cli_operator import cli_operator


class ssh_operator:
    def __init__(
        self,
        user_name: str,
        host_name: str,
        password: str,
        key_path: str = None,
        port: int = 22,
    ) -> None:
        """
        @param:
            user_name: (str) SSH接続のユーザー名
            host_name: (str) SSH接続先のホスト名
            key_path: (str) SSH秘密鍵のファイルパス
            port: (int) SSH接続のポート番号（デフォルトは22）
        """
        self.__user = user_name
        self.__host = host_name
        self.__pswd = password
        self.__key_path = key_path
        self.__port = port
        self.__state = False
        self.cli = cli_operator()
        self.init_ssh()

    def set_state(self, flag: bool) -> None:
        """
        SSH接続の状態を設定する
        @param:
            flag: (bool) SSH接続の状態
        """
        self.__state = flag

    def get_state(self) -> bool:
        """
        SSH接続の状態を取得する
        @return:
            (bool) SSH接続の状態
        """
        return self.__state

    def init_ssh(self):
        """
        SSH接続を初期化する
        """
        # sshコマンド
        self.cli.execute(
            "ssh " + f"-i {self.__key_path} "
            if (self.__key_path is not None)
            else "" + f"-p {self.__port} {self.__user}@{self.__host}"
        )
        # Are you sure you want to continue connecting (yes/no/[fingerprint])?
        self.cli.execute("yes")
        # user@host's password:
        answer = self.cli.execute(self.__pswd)
        if('Permission denied, please try again.' in answer[0]):
            raise SSHConectionError('password is not correct')
        self.set_state(True)

    def execute(self, command: str) -> tuple:
        """
        コマンドを実行する
        @param:
            command: (str) 実行するコマンド
        @return:
            (tuple) 標準出力と標準エラー出力のタプル
        """
        if not self.get_state():
            raise SSHConectionError("sshの接続が切れました")
        return self.cli.execute(command)

    def exit(self):
        """
        SSH接続を終了する
        """
        self.cli.close()


class SSHConectionError(Exception):
    pass
