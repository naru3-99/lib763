import socket


class UDPClient:
    def __init__(self, host: str, ports: list, buffer_size: int) -> None:
        self._host = host
        self._ports = ports
        self._buffer_size = buffer_size
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, message: str, encoding: str = "ascii") -> None:
        for port in self._ports:
            try:
                self._sock.sendto(message.encode(encoding), (self._host, port))
            except Exception as e:
                print(f"Error while sending message: {str(e)}")

    def __enter__(self) -> "UDPClient":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._sock.close()
