from lib763.net.UDPClient import UDPClient
import time
from typing import List, Any, Optional


class UDPControlClient(UDPClient):
    """A subclass of UDPClient that sends control commands at specified time intervals."""

    def __init__(self, host: str, ports: List[int], buffer_size: int) -> None:
        """
        Initialize the UDP control client.

        Args:
            host: The hostname or IP address.
            ports: The list of port numbers to send to.
            buffer_size: The size of the send buffer.
        """
        super().__init__(host, ports, buffer_size)
        self.FINISH_COMMAND = "\x02FINISH\x03"
        self.SAVE_COMMAND = "\x02SAVE\x03"
        self.loop = True

    def main(self, save_interval: float, finish_time: float) -> None:
        """
        The main method of the client. This method starts an infinite loop that sends SAVE_COMMAND at specified intervals and FINISH_COMMAND after a specified time.

        Args:
            save_interval: The time interval in seconds between sending SAVE_COMMAND.
            finish_time: The time in seconds after which FINISH_COMMAND is sent and the client is stopped.
        """
        start_time = time.time()
        last_save_time = start_time
        while self.loop:
            try:
                if time.time() - last_save_time > save_interval:
                    last_save_time = time.time()
                    self.send_message(self.SAVE_COMMAND)

                if time.time() - start_time > finish_time:
                    self.exit_all_client()
                    return
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error in main loop: {str(e)}")

    def exit(self) -> None:
        """
        Send the FINISH_COMMAND and exit the client.
        """
        self.loop = False
        self.__exit__(None, None, None)

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[Exception],
        traceback: Optional[Any],
    ) -> None:
        """
        Closes the socket connection when exiting a with statement.

        Args:
            exc_type: The type of exception.
            exc_value: The instance of exception.
            traceback: A traceback object encapsulating the call stack.
        """
        self._sock.close()
