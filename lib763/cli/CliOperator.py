import platform
import subprocess
from pexpect import spawn, exceptions


class CliOperator:
    """
    CLI (Command Line Interface)操作のための基底クラス。
    このクラス自体は抽象クラスであり、各メソッドは子クラスで実装すべきです。
    """

    def __init__(self, timeout=100):
        """
        CliOperatorの初期化
        :param timeout: 各コマンドの実行に対するタイムアウト（デフォルトは100秒）
        """
        self.timeout = timeout

    def execute(self, command: str, timeout=None):
        """
        コマンドを実行し、その出力とエラーを返します。
        このメソッドは具体的な実装が必要で、子クラスでオーバーライドされるべきです。
        :param command: 実行するコマンドの文字列
        :param timeout: コマンドの実行に対するタイムアウト（デフォルトはNone、親クラスのタイムアウトを使用）
        """
        raise NotImplementedError("Must override in a subclass")

    def get_process_id(self):
        """
        現在のプロセスのIDを取得します。
        このメソッドは具体的な実装が必要で、子クラスでオーバーライドされるべきです。
        :return: 現在のプロセスのID
        """
        raise NotImplementedError("Must override in a subclass")

    def close(self):
        """
        現在のプロセスを終了します。
        このメソッドは具体的な実装が必要で、子クラスでオーバーライドされるべきです。
        """
        raise NotImplementedError("Must override in a subclass")


class LinuxCliOperator(CliOperator):
    """
    Linux向けのCLI操作を行う具体的なクラス。
    親クラスのCliOperatorから派生しています。
    """

    def __init__(self, timeout=100):
        super().__init__(timeout)
        self.process = spawn("bash")

    def execute(self, command: str, timeout=None):
        self.process.sendline(command)
        try:
            self.process.expect(
                exceptions.EOF, timeout=timeout if timeout else self.timeout
            )
            return self.process.before.decode(), None
        except exceptions.EOF as e:
            return self.process.before.decode(), str(e)

    def get_process_id(self):
        return self.process.pid

    def close(self):
        if self.process.isalive():
            self.process.close()
        else:
            raise RuntimeError("Process is already closed")


class WindowsCliOperator(CliOperator):
    """
    Windows向けのCLI操作を行う具体的なクラス。
    親クラスのCliOperatorから派生しています。
    """

    def __init__(self, timeout=100):
        super().__init__(timeout)
        self.process = subprocess.Popen(
            "cmd",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def execute(self, command: str, timeout=None):
        self.process.stdin.write(command + "\n")
        try:
            out, err = self.process.communicate(
                timeout=timeout if timeout else self.timeout
            )
        except subprocess.TimeoutExpired as e:
            out, err = None, str(e)
        return out, err

    def get_process_id(self):
        return self.process.pid

    def close(self):
        if self.process.poll() is None:  # Check if process is still running
            self.process.stdin.close()
            self.process.wait()
        else:
            raise RuntimeError("Process is already closed")


def get_cli_operator(timeout=100):
    """
    現在のプラットフォームに適したCliOperatorのインスタンスを生成します。
    :param timeout: コマンドの実行に対するタイムアウト（デフォルトは100秒）
    :return: 対応したCliOperatorのインスタンス
    """
    if platform.system() == "Windows":
        return WindowsCliOperator(timeout)
    else:
        return LinuxCliOperator(timeout)
