import subprocess
import platform


class cli_operator:
    def __init__(self, timeout=100):
        self.timeout = timeout
        if platform.system() == "Windows":
            self.shell = "cmd"
        else:
            self.shell = "bash"

        self.process = subprocess.Popen(
            self.shell,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def execute(self, command: str) -> tuple:
        """
        コマンドを実行する
        @param:
            command: (str) 実行するコマンド
        @return:
            (tuple) 標準出力と標準エラー出力のタプル
        """
        try:
            return self.process.communicate(input=command + "\n", timeout=self.timeout)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process = subprocess.Popen(
                self.shell,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        return (None, 'timeout error')

    def get_process_id(self) -> int:
        """
        自分のプロセスIDを取得する
        @return:
            (int) プロセスID
        """
        return self.process.pid

    def close(self):
        """
        コマンドプロセスを終了する
        """
        self.process.stdin.close()
        self.process.wait()
