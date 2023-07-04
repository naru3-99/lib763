import subprocess
import threading
import time


class CLIManager:
    """
    CLIManager is a class that wraps subprocess commands execution
    and allows to process both stdout and stderr asynchronously
    and manage process timeout.
    """

    def execute(self, command, timeout=None):
        """
        Execute a shell command, asynchronously read stdout and stderr
        and kill the process if the timeout is exceeded.

        Args:
            command: Shell command to execute.
            timeout: Time in seconds after which the process should be killed if not finished.

        Returns:
            return code and process id.
        """

        # Start a new subprocess
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        pid = process.pid

        if timeout is not None:
            # If a timeout was specified, get the start time
            start_time = time.time()

        while process.poll() is None:
            if timeout is not None and time.time() - start_time > timeout:
                # If the process is not finished and the timeout was exceeded, kill the process
                process.kill()
                process.wait()
                break

        return process.returncode, pid
