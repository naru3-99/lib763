from lib763.net.UDPServer import UDPServer
from lib763.fs.save_load import append_str_to_file
from lib763.fs.fs import ensure_path_exists
from lib763.multp.multp import start_process
from queue import Queue
import threading
from typing import Callable, List


class UdpServerSaveFile(UDPServer):
    """A server for handling UDP packets and saving them to a file.

    Args:
        host (str): The host of the server.
        port (int): The port of the server.
        buffer_size (int): The maximum amount of data to be received at once.
        save_path (str): The path to the file where the data should be saved.
        edit_msg_func (Callable): A function to process the received data before saving.
    """

    def __init__(
        self,
        host: str,
        port: int,
        buffer_size: int,
        save_path: str,
        edit_msg_func: Callable,
    ) -> None:
        super().__init__(host, port, buffer_size)
        self.save_path = save_path
        self.saver = OrderedSaver(self.save_path, edit_msg_func)
        self.FINISH_COMMAND = "\x02FINISH\x03"
        self.SAVE_COMMAND = "\x02SAVE\x03"
        self.loop = True
        self.decoded_msg_ls = []

    def main(self) -> None:
        """The main loop of the server, receiving and processing data."""
        ensure_path_exists(self.save_path)
        self.saver.start()
        while self.loop:
            try:
                decoded_msg = self.receive_udp_packet().decode()
                if decoded_msg == self.FINISH_COMMAND:
                    self.exit_this_server()
                    return
                elif decoded_msg == self.SAVE_COMMAND:
                    if len(self.decoded_msg_ls) != 0:
                        self.saver.append_data(self.decoded_msg_ls.copy())
                        self.decoded_msg_ls.clear()
                else:
                    self.decoded_msg_ls.append(decoded_msg)
            except Exception as e:
                print(f"Error in main loop: {str(e)}")

    def exit_this_server(self) -> None:
        """Exits the server and finishes saving any remaining data."""
        if len(self.decoded_msg_ls) != 0:
            self.saver.append_data(self.decoded_msg_ls.copy())
            self.decoded_msg_ls.clear()
        self.__exit__(None, None, None)
        self.saver.stop()
        self.loop = False


class OrderedSaver:
    def __init__(self, save_path: str, edit_msg_func: Callable) -> None:
        """OrderedSaverのコンストラクタ.

        Args:
            save_path (str): ファイルパス.
            edit_msg_func (Callable): メッセージ編集関数.
        """
        self.save_path = save_path
        self.func = edit_msg_func
        self.queue = Queue()

    def append_data(self, copied_data: List[str]) -> None:
        """データをキューに追加します.

        Args:
            copied_data (List[str]): データ.
        """
        self.queue.put(copied_data)

    def stop(self):
        """ファイル書き込みを停止します."""
        self.queue.put(None)
        self.process.join()

    def start(self) -> None:
        """
        ファイル書き込みを開始します.
        """
        self.thread = threading.Thread(target=self.main)
        self.thread.start()

    def write(self, data_ls: list) -> None:
        """データをファイルに書き込みます.

        Args:
            data_ls (list): データ.
        """
        save_str = ""
        for row in [self.func(row) for row in data_ls]:
            if row is not None:
                save_str += row + "\n"
        append_str_to_file(save_str, self.save_path)

    def main(self) -> None:
        """キューから順にデータを取り出し、ファイルに書き込みます."""
        while True:
            data_ls = self.queue.get()
            if data_ls is None:
                break
            self.write(data_ls)
