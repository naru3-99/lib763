import subprocess


class cmd_operator:
    def __init__(self):
        self.process = subprocess.Popen(
            "cmd",
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
        return self.process.communicate(input=command + "\n")

    def close(self):
        """
        コマンドプロセスを終了する
        """
        self.process.stdin.close()
        self.process.wait()
