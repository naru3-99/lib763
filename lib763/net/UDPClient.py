import socket
from typing import List, Any, Optional, Tuple


class UDPClient:
    """A UDP client for sending messages to a list of ports on a host.

    Attributes:
        host: A string representing the host to which messages are to be sent.
        ports: A list of integers representing the ports on the host.
        buffer_size: An integer representing the buffer size.
    """

    def __init__(self, host: str, ports: List[int], buffer_size: int) -> None:
        """
        Initializes UDPClient with the host, ports, and buffer size.

        Args:
            host: A string representing the host to which messages are to be sent.
            ports: A list of integers representing the ports on the host.
            buffer_size: An integer representing the buffer size.
        """
        self._host = host
        self._ports = ports
        self._buffer_size = buffer_size
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, message: str, encoding: str = "ascii") -> None:
        """
        Sends a message to all the ports on the host.

        Args:
            message: A string representing the message to be sent.
            encoding: A string representing the encoding used to encode the message.

        Raises:
            Exception: An exception is raised if there is an error while sending the message.
        """
        for port in self._ports:
            try:
                self._sock.sendto(message.encode(encoding), (self._host, port))
            except Exception as e:
                print(f"Error while sending message: {str(e)}")

    def __enter__(self) -> "UDPClient":
        """
        Enables use of UDPClient in a with statement.

        Returns:
            self: The instance of UDPClient.
        """
        return self

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
