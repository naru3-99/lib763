import socket


class udp_server:
    def __init__(self, host: str, port: int, buffer_size: int) -> None:
        """

        @Args:
            host (str): ホスト名またはIPアドレス
            port (int): ポート番号
            buffer_size (int): 受信バッファのサイズ
        """
        self._host = host
        self._port = port
        self._buffer_size = buffer_size
        self._sock = None

    def __enter__(self) -> "udp_server":
        """
        コンテキストマネージャの開始時に呼び出されるメソッド
        サーバーの初期化を行う

        @Returns:
            UDPServer: 自身のインスタンス
        """
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((self._host, self._port))
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        コンテキストマネージャの終了時に呼び出されるメソッド
        ソケットをクローズする
        """
        self._sock.close()

    def receive_udp_packet(self) -> bytes:
        """
        UDPパケットを受信する

        @Returns:
            bytes: 受信したパケットのデータ
        """
        rcv_data, addr = self._sock.recvfrom(self._buffer_size)
        return rcv_data
