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
            A dictionary with stdout, stderr, return code, and process id.
        """

        # Start a new subprocess
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        pid = process.pid
        stdout_lock = threading.Lock()
        stderr_lock = threading.Lock()

        def stream_reader(stream, output_list, lock):
            """
            Read lines from a stream (stdout or stderr) and add them to the output_list.

            Args:
                stream: Stream to read from.
                output_list: List to add read lines to.
                lock: Lock object for synchronizing access to the output_list.
            """
            while not stream.closed:
                line = stream.readline()
                if not line:
                    break
                with lock:
                    output_list.append(line.decode("utf8"))

        stdout_lines = []
        stderr_lines = []
        # Start two threads that will read stdout and stderr
        stdout_thread = threading.Thread(
            target=stream_reader, args=(process.stdout, stdout_lines, stdout_lock)
        )
        stderr_thread = threading.Thread(
            target=stream_reader, args=(process.stderr, stderr_lines, stderr_lock)
        )
        stdout_thread.start()
        stderr_thread.start()

        if timeout is not None:
            # If a timeout was specified, get the start time
            start_time = time.time()

        while process.poll() is None:
            if timeout is not None and time.time() - start_time > timeout:
                # If the process is not finished and the timeout was exceeded, kill the process
                process.kill()
                process.wait()
                break

        # Wait for the threads to finish
        stdout_thread.join()
        stderr_thread.join()

        with stdout_lock:
            stdout = "".join(stdout_lines)

        with stderr_lock:
            stderr = "".join(stderr_lines)

        return {
            "stdout": stdout,
            "stderr": stderr,
            "returncode": process.returncode,
            "pid": pid,
        }
