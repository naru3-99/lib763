from typing import List, Tuple
import pexpect
import time


class CliExpect:
    """A class used to manage Command Line Interface interactions.

    Attributes:
        timeout (int): The maximum time to wait for the command to execute. Default is 100 seconds.
        sleep_interval (float): The time to sleep between sending each input. Default is 0.05 seconds.
    """

    def __init__(self, timeout: int = 2, sleep_interval: float = 0.05):
        """Initializes the CliExpect with the given timeout and sleep interval.

        Args:
            timeout (int): The maximum time to wait for the command to execute. Default is 100 seconds.
            sleep_interval (float): The time to sleep between sending each input. Default is 0.05 seconds.
        """
        self.timeout = timeout
        self.sleep_interval = sleep_interval

    def execute(self, command: str, user_inputs: List[str]) -> Tuple[int, int]:
        """Executes the command and provides the user inputs when needed.

        Args:
            command (str): The command to be executed.
            user_inputs (List[str]): A list of inputs to be provided to the command.

        Returns:
            Tuple[int, int]: The exit code from the executed command and the process id of the executed command.
        """
        child = pexpect.spawn(f"bash -c '{command}'", timeout=self.timeout)

        # Waiting for each expected output and sending corresponding input
        for input_data in user_inputs:
            try:
                child.sendline(input_data)
                time.sleep(
                    self.sleep_interval
                )  # wait a bit before sending the next command
            except pexpect.TIMEOUT:
                raise TimeoutError(
                    f"The command took longer than {self.timeout} seconds."
                )

        child.close(
            force=True
        )  # forcefully close the child if it doesn't respond to EOF
        exit_code = child.exitstatus
        return exit_code, child.pid
