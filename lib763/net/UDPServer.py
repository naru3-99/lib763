import socket
import time
from typing import Optional, Any, Tuple, Type


class UDPServer:
    """A server for handling UDP packets.

    Args:
        host (str): The host of the server.
        port (int): The port of the server.
        buffer_size (int): The maximum amount of data to be received at once.
    """

    def __init__(self, host: str, port: int, buffer_size: int, timeout=None) -> None:
        """Initialize the server with host, port and buffer size.

        Args:
            host (str): The host of the server.
            port (int): The port of the server.
            buffer_size (int): The maximum amount of data to be received at once.
        """
        self._host = host
        self._port = port
        self._buffer_size = buffer_size
        to = timeout if timeout is not None else 60
        if not self.init_server(to):
            raise TimeoutError("UDP server timeout to bind")

    def init_server(self, timeout=60):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind((self._host, self._port))
                return True
            except OSError as e:
                if e.winerror == 10048:
                    time.sleep(1)
                    continue
                else:
                    raise e
        return False

    def receive_udp_packet(self, timeout: float = None) -> Optional[bytes]:
        """Receive a UDP packet from the socket.

        Args:
            timeout (float, optional): The timeout in seconds. Defaults to None.

        Returns:
            Optional[bytes]: The received data, None if an error occurred.
        """
        try:
            self._sock.settimeout(timeout)
            rcv_data, _ = self._sock.recvfrom(self._buffer_size)
            return rcv_data
        except socket.timeout:
            return None
        except Exception as e:
            return None

    def __enter__(self) -> "UDPServer":
        """Enter the context of the server, allowing use with 'with' statement.

        Returns:
            UDPServer: The server instance.
        """
        return self

    def __exit__(
        self, exc_type: Type[BaseException], exc_value: BaseException, traceback: Any
    ) -> None:
        """Exit the context of the server, allowing use with 'with' statement.

        Args:
            exc_type (Type[BaseException]): The type of exception.
            exc_value (BaseException): The instance of exception.
            traceback (Any): A traceback object.
        """
        self._sock.close()
