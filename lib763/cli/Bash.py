import subprocess
from subprocess import TimeoutExpired
from typing import Tuple, List, Optional


class Bash:
    def __init__(self, cwd: str, sudo_password: str) -> None:
        """Bashコマンドを実行するクラス。

        Args:
            cwd (str): 初期の作業ディレクトリ。
            sudo_password (str): `sudo`コマンド実行時に必要なパスワード。
        """
        self.current_directory = cwd
        self.sudo_password = sudo_password

    def cd(self, dir_path: str) -> None:
        """作業ディレクトリを更新する。

        Args:
            dir_path (str): 移動先のディレクトリのパス。
        """
        self.current_directory = dir_path

    def execute(
        self, command: str, user_input: Optional[List[str]] = None, timeout: int = 5
    ) -> Tuple[int, int, str, str]:
        """指定したシェルコマンドを実行する。

        Args:
            command (str): 実行するコマンド。
            user_input (Optional[List[str]]): コマンド実行時のユーザー入力。Noneの場合、ユーザー入力は不要。
            timeout (int): コマンドの最大実行時間（秒）。

        Returns:
            Tuple[int, int, str, str]: プロセスID、終了コード、標準出力、標準エラー出力。
        """
        try:
            proc = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.current_directory,
                text=True,
                shell=True,
            )
            pid = proc.pid

            if user_input is not None:
                user_input = "\n".join(user_input).encode("utf-8")
                stdout, stderr = proc.communicate(user_input, timeout=timeout)
            else:
                stdout, stderr = proc.communicate(timeout=timeout)

        except TimeoutExpired:
            return proc.pid, proc.returncode, "", "Command execution timed out"
        return pid, proc.returncode, stdout, stderr

    def sudo_execute(
        self, command: str, user_input: Optional[List[str]] = None, timeout: int = 5
    ) -> Tuple[int, int, str, str]:
        """指定したシェルコマンドを`sudo`で実行する。

        Args:
            command (str): 実行するコマンド。
            user_input (Optional[List[str]]): コマンド実行時のユーザー入力。Noneの場合、ユーザー入力は不要。
            timeout (int): コマンドの最大実行時間（秒）。

        Returns:
            Tuple[int, int, str, str]: プロセスID、終了コード、標準出力、標準エラー出力。
        """
        return self.execute(
            f"echo {self.sudo_password} | sudo -S {command}", user_input, timeout
        )
