import subprocess as sbp
import os
from typing import Tuple, List, Optional


class Bash:
    """A class for executing Bash commands.

    Attributes:
        current_directory: The current working directory for executing commands.
        sudo_password: The password to use for sudo commands.
    """

    def __init__(
        self, cwd: Optional[str] = None, sudo_password: Optional[str] = None
    ) -> None:
        """Initializes the Bash object.

        Args:
            cwd: The current working directory. Defaults to the current directory.
            sudo_password: The password for sudo. Defaults to None.

        """
        self.current_directory = (
            os.path.abspath(cwd) if cwd is not None else os.getcwd()
        )
        self.sudo_password = sudo_password

    def cd(self, dir_path: str) -> None:
        """Changes the current working directory.

        Args:
            dir_path: The directory path to change to.

        Raises:
            FileNotFoundError: If the directory does not exist.
        """
        abs_path = os.path.abspath(dir_path)
        if os.path.exists(abs_path):
            self.current_directory = abs_path
        else:
            raise FileNotFoundError(f"{abs_path} not found.")

    def execute(
        self, command: str, user_input: Optional[List[str]] = None, timeout: int = 5
    ) -> Tuple[int, int, str, str]:
        """Executes a shell command.

        Args:
            command: The command to execute.
            user_input: A list of strings for user input to the command. Defaults to None.
            timeout: The time in seconds to wait for the command. Defaults to 5.

        Returns:
            A tuple containing:
                - Process ID
                - Return code
                - Standard output
                - Standard error

        Raises:
            subprocess.TimeoutExpired: If the command times out.
            Exception: For other exceptions from subprocess.
        """
        try:
            proc = sbp.Popen(
                command,
                stdin=sbp.PIPE,
                stdout=sbp.PIPE,
                stderr=sbp.PIPE,
                cwd=self.current_directory,
                text=True,
                shell=True,
            )
            pid = proc.pid

            if user_input is not None:
                user_input_str = "\n".join(user_input)
                stdout, stderr = proc.communicate(user_input_str, timeout=timeout)
            else:
                stdout, stderr = proc.communicate(timeout=timeout)

        except sbp.TimeoutExpired:
            return proc.pid, proc.returncode, "", "Command execution timed out"
        except Exception as e:
            return 0, -1, "", str(e)

        return pid, proc.returncode, stdout, stderr

    def sudo_execute(
        self, command: str, user_input: Optional[List[str]] = None, timeout: int = 5
    ) -> Tuple[int, int, str, str]:
        """Executes a sudo command.

        Args:
            command: The command to execute with sudo.
            user_input: A list of strings for user input to the command. Defaults to None.
            timeout: The time in seconds to wait for the command. Defaults to 5.

        Returns:
            A tuple containing:
                - Process ID
                - Return code
                - Standard output
                - Standard error

        Raises:
            NoSudoPasswordError: If no sudo password is provided.
        """
        if self.sudo_password is None:
            raise NoSudoPasswordError("No sudo password input")

        return self.execute(
            f"echo {self.sudo_password} | sudo -S {command}", user_input, timeout
        )


class NoSudoPasswordError(Exception):
    """Exception raised for missing sudo password."""

    pass
