import subprocess
import time


class CliOperator:
    """CLI(Command Line Interface)を操作するクラス"""

    def __init__(self):
        self.process = None

    def execute(self, command, timeout=None):
        """指定されたコマンドを実行し、その結果を返します

        引数:
            command (str): 実行するコマンド。
            timeout (int, optional): コマンドの実行が終了するまでの最大待ち時間（秒）。
                指定しない場合、またはNoneの場合、無制限に待つ。

        戻り値:
            stdout (str): コマンドの標準出力。
            stderr (str): コマンドの標準エラー出力。
            returncode (int): コマンドの終了ステータス。
            pid (int): 実行したプロセスのID。

        例外:
            subprocess.TimeoutExpired: コマンドの実行がtimeoutで指定した時間を超えた場合に発生します。

        注意:
            タイムアウトが発生した場合、プロセスは強制的に終了されます。
        """
        try:
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True,
            )
            pid = self.process.pid

            if timeout is None:
                stdout, stderr = self.process.communicate(timeout=timeout)
                returncode = self.process.returncode
            else:
                time.sleep(timeout)
                self.process.terminate()
                stdout, stderr = self.process.communicate(timeout=timeout)
                returncode = self.process.returncode

        except subprocess.TimeoutExpired:
            self.process.kill()
            stdout, stderr = self.process.communicate(timeout=timeout)
            returncode = self.process.returncode
        finally:
            self.process = None

        return stdout, stderr, returncode, pid
