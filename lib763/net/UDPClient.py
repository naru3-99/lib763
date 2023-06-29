import socket


class UDPClient:
    """UDPクライアントを管理するクラス。"""

    def __init__(self, host: str, ports: list, buffer_size: int) -> None:
        """UDPクライアントの初期設定を行います。

        Args:
            host: ホスト名またはIPアドレス
            ports: 送信先のポート番号のリスト
            buffer_size: 送信バッファのサイズ
        """
        self._host = host
        self._ports = ports
        self._buffer_size = buffer_size
        self._sock = None

    def close(self):
        """socketを閉じて終了する"""
        self._sock.close()

    def send_message(self, message: str, encoding: str = "ascii") -> None:
        """指定されたメッセージを全てのポートに送信します。

        Args:
            message: 送信するメッセージ
        """
        for port in self._ports:
            self._sock.sendto(message.encode(encoding), (self._host, port))

    def __enter__(self) -> "UDPClient":
        """コンテキストマネージャの開始時にソケットを初期化します。

        Returns:
            自身のインスタンス
        """
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """コンテキストマネージャの終了時にソケットをクローズします。"""
        self._sock.close()
