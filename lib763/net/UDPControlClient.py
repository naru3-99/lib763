from lib763.net.UDPClient import UDPClient
import time


class UDPControlClient(UDPClient):
    """
    A subclass of UDPClient that sends control commands at specified time intervals.
    """

    def __init__(self, host: str, ports: list, buffer_size: int) -> None:
        """
        Initialize the UDP control client.

        Args:
            host (str): The hostname or IP address.
            ports (list): The list of port numbers to send to.
            buffer_size (int): The size of the send buffer.
        """
        super().__init__(host, ports, buffer_size)
        self.FINISH_COMMAND = "\x02FINISH\x03"
        self.SAVE_COMMAND = "\x02SAVE\x03"

    def main(self, save_interval: float, finish_time: float) -> None:
        """
        The main method of the client. This method starts an infinite loop that sends SAVE_COMMAND at specified intervals and FINISH_COMMAND after a specified time.

        Args:
            save_interval (float): The time interval in seconds between sending SAVE_COMMAND.
            finish_time (float): The time in seconds after which FINISH_COMMAND is sent and the client is stopped.
        """
        start_time = time.time()
        last_save_time = start_time
        while True:
            try:
                if time.time() - last_save_time > save_interval:
                    last_save_time = time.time()
                    self.send_message(self.SAVE_COMMAND)

                if time.time() - start_time > finish_time:
                    self.send_message(self.SAVE_COMMAND)
                    self.send_message(self.FINISH_COMMAND)
                    self.__exit__(None, None, None)
                    return
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error in main loop: {str(e)}")
