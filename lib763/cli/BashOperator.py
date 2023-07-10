import subprocess
import threading
import time


class BashOperator:
    """Class to operate bash shell using Python.

    Attributes:
        shell (subprocess.Popen): The subprocess instance of bash shell.
        command_end_suffix (int): The suffix appended to the command end string for distinguishing commands.
        wait (float): The time to wait after each command execution.
        cwd (str): The current working directory of the bash shell.
    """

    def __init__(self, time_to_wait=0.5):
        """Initializes a BashOperator instance with a bash shell subprocess.

        Args:
            time_to_wait (float, optional): The time to wait after each command execution. Default is 0.5.
        """
        self.shell = subprocess.Popen(
            "bash",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )
        self.command_end_suffix = 0
        self.wait = time_to_wait
        self.cwd = self.get_current_dir()

    def execute(self, command:str, timeout=10):
        """Executes a bash command.

        Args:
            command (str): The bash command to execute.
            timeout (int, optional): The maximum time to wait for the command to execute. Default is 10.

        Raises:
            RuntimeError: If the command execution exceeds the timeout.
        """
        self.cwd = self.get_current_dir()
        self.command_end_suffix += 1

        def target():
            self.shell.stdin.write(
                command + " 2> >(tee /dev/fd/2; echo 'END_OF_STDERR')\n"
            )
            self.shell.stdin.write(f"echo END_OF_COMMAND{self.command_end_suffix}\n")
            self.shell.stdin.flush()

        thread = threading.Thread(target=target)
        thread.start()

        try:
            thread.join(timeout)
            if thread.is_alive():
                raise RuntimeError(
                    "Command '{}' timed out after {} seconds".format(command, timeout)
                )
        except RuntimeError as e:
            self.shell.stdin.write(f"echo 'END_OF_STDERR' >&2\n")
            self.shell.stdin.write(f"echo END_OF_COMMAND{self.command_end_suffix}\n")
            self.shell.stdin.flush()
            self.reset()
            raise e
        time.sleep(self.wait)

    def get_current_dir(self):
        """Gets the current working directory of the bash shell.

        Returns:
            str: The current working directory.
        """
        self.shell.stdin.write("pwd\n")
        self.command_end_suffix += 1
        self.shell.stdin.write(f"echo END_OF_COMMAND{self.command_end_suffix}\n")
        self.shell.stdin.flush()
        output = []
        while True:
            line = self.shell.stdout.readline()
            if f"END_OF_COMMAND{self.command_end_suffix}" in line:
                break
            output.append(line)
        return output[-1].strip()

    def change_dir(self, new_dir:str):
        """Changes the working directory of the bash shell.

        Args:
            new_dir (str): The new directory to change to.
        """
        self.execute(f"cd {new_dir}")

    def reset(self):
        """Resets the bash shell subprocess."""
        self.shell.terminate()
        self.shell = subprocess.Popen(
            "bash",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )
        self.change_dir(self.cwd)

    def get_stdout(self):
        """Gets the standard output of the last executed command.

        Returns:
            str: The standard output.
        """
        output = []
        while True:
            line = self.shell.stdout.readline()
            if f"END_OF_COMMAND{self.command_end_suffix}" in line:
                break
            output.append(line)
        return "".join(output)

    def get_stderr(self):
        """Gets the standard error of the last executed command.

        Returns:
            str: The standard error.
        """
        output = []
        while True:
            line = self.shell.stderr.readline()
            if f"END_OF_STDERR{self.command_end_suffix}" in line:
                break
            output.append(line)
        return "".join(output)
