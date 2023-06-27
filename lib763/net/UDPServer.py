import socket


class UDPServer:
    """UDPサーバーを管理するクラス。"""

    def __init__(self, host: str, port: int, buffer_size: int) -> None:
        """UDPサーバーの初期設定を行います。

        Args:
            host: ホスト名またはIPアドレス
            port: ポート番号
            buffer_size: 受信バッファのサイズ
        """
        self._host = host
        self._port = port
        self._buffer_size = buffer_size
        self._sock = None

    def __enter__(self) -> "UDPServer":
        """コンテキストマネージャの開始時にソケットを初期化します。

        Returns:
            自身のインスタンス
        """
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((self._host, self._port))
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """コンテキストマネージャの終了時にソケットをクローズします。"""
        self._sock.close()

    def receive_udp_packet(self) -> bytes:
        """UDPパケットを受信します。

        Returns:
            受信したパケットのデータ
        """
        rcv_data, addr = self._sock.recvfrom(self._buffer_size)
        return rcv_data
