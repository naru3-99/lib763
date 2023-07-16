from lib763.net.UDPServer import UDPServer
from lib763.fs.save_load import append_str_to_file


class UdpServerSaveFile(UDPServer):
    """
    A UDP server class that saves received data to a file.
    This class is designed to be subclassed, and requires the method `edit_save_str` to be implemented in subclasses.
    """

    def __init__(self, host: str, port: int, buffer_size: int) -> None:
        """
        Initialize the server.

        Args:
            host (str): The hostname or IP address.
            port (int): The port number.
            buffer_size (int): The size of the receive buffer.
        """
        super().__init__(host, port, buffer_size)
        self.FINISH_COMMAND = "\x02FINISH\x03"
        self.SAVE_COMMAND = "\x02SAVE\x03"

    def edit_save_str(self, recieved_str: str) -> str:
        """Edit the received string before saving it.
        This method must be implemented by subclasses.

        Args:
            recieved_str (str): The received string.

        Returns:
            str: The edited string.

        Raises:
            NotImplementedError: If this method is not implemented in a subclass.
        """
        raise NotImplementedError("This method must be implemented by subclasses")

    def main(self, save_path: str) -> None:
        """The main method of the server.
        This method starts an infinite loop that listens for incoming packets and processes them.

        Args:
            save_path (str): The path to the file where the received data will be saved.
        """
        decoded_msg_ls = []
        try:
            while True:
                decoded_msg = self.receive_udp_packet().decode()
                if decoded_msg == self.FINISH_COMMAND:
                    self.__exit__(None, None, None)
                    return
                elif decoded_msg == self.SAVE_COMMAND:
                    append_str_to_file(
                        "\n".join([self.edit_save_str(msg) for msg in decoded_msg_ls]),
                        save_path,
                    )
                    decoded_msg_ls.clear()
                else:
                    decoded_msg_ls.append(decoded_msg)
        except Exception as e:
            print(f"Error in main loop: {str(e)}")
