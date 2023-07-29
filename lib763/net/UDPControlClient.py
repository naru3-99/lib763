import time
from typing import List
from multiprocessing import Queue

from lib763.net.UDPClient import UDPClient
from lib763.net.CONST import SAVE_COMMAND, FINISH_COMMAND, STOP_COMMAND


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
        self.queue = Queue()

    def main(self, save_interval: float, finish_time: float) -> None:
        """
        The main method of the client. This method starts an infinite loop that sends SAVE_COMMAND at specified intervals and FINISH_COMMAND after a specified time.

        Args:
            save_interval: The time interval in seconds between sending SAVE_COMMAND.
            finish_time: The time in seconds after which FINISH_COMMAND is sent and the client is stopped.
        """
        start_time = time.time()
        last_save_time = start_time
        while True:
            if not self.queue.empty() and self.queue.get() == STOP_COMMAND:
                break
            try:
                if time.time() - last_save_time > save_interval:
                    last_save_time = time.time()
                    self.send_message(SAVE_COMMAND)

                if time.time() - start_time > finish_time:
                    self.stop_loop()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error in ctrl-client-main loop: {str(e)}")
        self._exit()

    def stop_loop(self) -> None:
        self.queue.put(STOP_COMMAND)

    def _exit(self) -> None:
        """
        Send the FINISH_COMMAND and exit the client.
        """
        self.send_message(FINISH_COMMAND)
        self.__exit__(None, None, None)
