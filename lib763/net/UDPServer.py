import socket
from typing import Optional


class UDPServer:
    """A class to manage a UDP server."""

    def __init__(self, host: str, port: int, buffer_size: int) -> None:
        """
        Initialize the UDP server.

        Args:
            host (str): The hostname or IP address.
            port (int): The port number.
            buffer_size (int): The size of the receive buffer.
        """
        self._host = host
        self._port = port
        self._buffer_size = buffer_size
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((self._host, self._port))

    def receive_udp_packet(self) -> Optional[bytes]:
        """
        Receive a UDP packet.

        Returns:
            bytes: The data of the received packet, or None if an error occurred.
        """
        try:
            rcv_data, addr = self._sock.recvfrom(self._buffer_size)
            return rcv_data
        except Exception as e:
            print(f"Error while receiving packet: {str(e)}")
            return None

    def __enter__(self) -> "UDPServer":
        """
        Initialize the context manager.

        Returns:
            UDPServer: The instance of this class.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Close the socket when exiting the context manager."""
        self._sock.close()
