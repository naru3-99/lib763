import socket


class UDPClient:
    def __init__(self, host: str, ports: list, buffer_size: int) -> None:
        """
        UDPクライアントの初期化

        @Args:
            host (str): ホスト名またはIPアドレス
            ports (list): 送信先のポート番号のリスト
            buffer_size (int): 送信バッファのサイズ
        """
        self._host = host
        self._ports = ports
        self._buffer_size = buffer_size
        self._sock = None

    def __enter__(self) -> "UDPClient":
        """
        コンテキストマネージャの開始時に呼び出されるメソッド
        クライアントの初期化を行う

        @Returns:
            UDPClient: 自身のインスタンス
        """
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        コンテキストマネージャの終了時に呼び出されるメソッド
        ソケットをクローズする
        """
        self._sock.close()

    def send_msg(self, msg: str) -> None:
        """
        メッセージを送信する

        @Args:
            msg (str): 送信するメッセージ
        """
        for port in self._ports:
            self._sock.sendto(msg.encode("ascii"), (self._host, port))
