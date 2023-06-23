from lib763.cli.cli_operator import cli_operator


class ssh_operator:
    def __init__(self, user_name: str, host_name: str, key_path: str, port: int = 22) -> None:
        """
        @param:
            user_name: (str) SSH接続のユーザー名
            host_name: (str) SSH接続先のホスト名
            key_path: (str) SSH秘密鍵のファイルパス
            port: (int) SSH接続のポート番号（デフォルトは22）
        """
        self.cmd = cli_operator()
        self.__user = user_name
        self.__host = host_name
        self.__key_path = key_path
        self.__port = port
        self.__state = False

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

    def __init_ssh(self):
        """
        SSH接続を初期化する
        """
        self.cmd.execute(f"ssh -i {self.__key_path} -p {self.__port} {self.__user}@{self.__host}")
        self.__state = True

    def execute(self, command: str) -> tuple:
        """
        コマンドを実行する
        @param:
            command: (str) 実行するコマンド
        @return:
            (tuple) 標準出力と標準エラー出力のタプル
        """
        if not self.get_state():
            self.__init_ssh()
        return self.cmd.execute(command)

    def exit(self):
        """
        SSH接続を終了する
        """
        self.cmd.close()
