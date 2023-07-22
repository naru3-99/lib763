import socket
from typing import Optional


class UDPServer:
    def __init__(self, host: str, port: int, buffer_size: int) -> None:
        self._host = host
        self._port = port
        self._buffer_size = buffer_size
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((self._host, self._port))

    def receive_udp_packet(self) -> Optional[bytes]:
        try:
            rcv_data, _ = self._sock.recvfrom(self._buffer_size)
            return rcv_data
        except Exception as e:
            print(f"Error while receiving packet: {str(e)}")
            return None

    def __enter__(self) -> "UDPServer":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._sock.close()
