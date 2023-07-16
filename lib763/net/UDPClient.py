import socket
from typing import Optional


class UDPClient:
    """A class to manage a UDP client."""

    def __init__(self, host: str, ports: list, buffer_size: int) -> None:
        """
        Initialize the UDP client.

        Args:
            host (str): The hostname or IP address.
            ports (list): The list of port numbers to send to.
            buffer_size (int): The size of the send buffer.
        """
        self._host = host
        self._ports = ports
        self._buffer_size = buffer_size
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, message: str, encoding: str = "ascii") -> None:
        """
        Send the specified message to all ports.

        Args:
            message (str): The message to send.
            encoding (str): The string encoding. Default is "ascii".
        """
        for port in self._ports:
            try:
                self._sock.sendto(message.encode(encoding), (self._host, port))
            except Exception as e:
                print(f"Error while sending message: {str(e)}")

    def __enter__(self) -> "UDPClient":
        """
        Initialize the context manager.

        Returns:
            UDPClient: The instance of this class.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Close the socket when exiting the context manager."""
        self._sock.close()
