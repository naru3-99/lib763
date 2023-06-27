import platform
import subprocess

from pexpect import spawn
from pexpect.exceptions import EOF


class CliOperator:
    """
    CLI (Command Line Interface)操作のための親クラス
    各メソッドは子クラスでオーバーライドされるべき
    """

    def __init__(self, timeout=100):
        """
        初期化処理
        :param timeout: コマンドのタイムアウト（デフォルトは100秒）
        """
        self.timeout = timeout

    def execute(self, command: str, timeout=None):
        """
        コマンドの実行
        :param command: 実行するコマンド
        :param timeout: コマンドのタイムアウト（デフォルトはNone、親クラスのタイムアウトを使用）
        """
        raise NotImplementedError("Must override in a subclass")

    def get_process_id(self):
        """
        プロセスIDの取得
        :return: プロセスID
        """
        raise NotImplementedError("Must override in a subclass")

    def close(self):
        """
        プロセスの終了
        """
        raise NotImplementedError("Must override in a subclass")


class LinuxCliOperator(CliOperator):
    """
    Linux向けのCLI操作クラス
    """

    def __init__(self, timeout=100):
        """
        初期化処理
        :param timeout: コマンドのタイムアウト（デフォルトは100秒）
        """
        super().__init__(timeout)
        self.process = spawn("bash")

    def execute(self, command: str, timeout=None):
        """
        コマンドの実行
        :param command: 実行するコマンド
        :param timeout: コマンドのタイムアウト（デフォルトはNone、親クラスのタイムアウトを使用）
        :return: 実行結果の文字列
        """
        self.process.sendline(command)
        try:
            self.process.expect(EOF, timeout=timeout if timeout else self.timeout)
            return self.process.before.decode(), None
        except EOF:
            return self.process.before.decode(), None

    def get_process_id(self):
        """
        プロセスIDの取得
        :return: プロセスID
        """
        return self.process.pid

    def close(self):
        """
        プロセスの終了
        """
        self.process.close()


class WindowsCliOperator(CliOperator):
    """
    Windows向けのCLI操作クラス
    """

    def __init__(self, timeout=100):
        """
        初期化処理
        :param timeout: コマンドのタイムアウト（デフォルトは100秒）
        """
        super().__init__(timeout)
        self.process = subprocess.Popen(
            "cmd",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def execute(self, command: str, timeout=None):
        """
        コマンドの実行
        :param command: 実行するコマンド
        :param timeout: コマンドのタイムアウト（デフォルトはNone、親クラスのタイムアウトを使用）
        :return: 実行結果の文字列
        """
        self.process.stdin.write(command + "\n")
        out, err = self.process.communicate(
            timeout=timeout if timeout else self.timeout
        )
        return out, err

    def get_process_id(self):
        """
        プロセスIDの取得
        :return: プロセスID
        """
        return self.process.pid

    def close(self):
        """
        プロセスの終了
        """
        self.process.stdin.close()
        self.process.wait()


def get_cli_operator(timeout=100):
    """
    現在のプラットフォームに応じたCliOperatorのインスタンスを取得
    :param timeout: コマンドのタイムアウト（デフォルトは100秒）
    :return: 対応したCliOperatorのインスタンス
    """
    if platform.system() == "Windows":
        return WindowsCliOperator(timeout)
    else:
        return LinuxCliOperator(timeout)
