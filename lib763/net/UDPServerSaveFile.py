from multiprocessing import Queue
from typing import Callable
import time

from lib763.fs.fs import ensure_path_exists
from lib763.fs.save_load import append_str_to_file
from lib763.multp.multp import start_process
from lib763.net.UDPServer import UDPServer

STOP_COMMAND = "\x02STOP\x03"


class UdpServerSaveFile(UDPServer):
    def __init__(
        self,
        host: str,
        port: int,
        udp_buffer_size: int,
        edit_msg_func: Callable,
        msg_buf_size: int,
    ) -> None:
        super().__init__(host, port, udp_buffer_size)
        self.loop = Queue()
        self.save_msgs_q = None
        self.save_path_q = Queue()
        self.msgs_buffer = []
        self.edit_func = edit_msg_func
        self.msg_buf_size = msg_buf_size

    def init_save_file(self, path):
        self.save_path_q.put(path)

    def start_save_proc(self):
        # when added new path to save_path_q
        # finish current msgs queue
        if not self.save_msgs_q is None:
            self.save_msgs()
            self.save_msgs_q.put(STOP_COMMAND)
        # create new queue and process
        path = self.save_path_q.get()
        ensure_path_exists(path)
        self.save_msgs_q = Queue()
        start_process(save_proc, self.save_msgs_q, path, self.edit_func)

    def main(self) -> None:
        # pathがセットされるまで待つ
        while self.save_path_q.empty():
            time.sleep(1)
        self.start_save_proc()

        # main loop
        while self.loop.empty():
            try:
                # pathが更新されているか確認する
                if not self.save_path_q.empty():
                    self.start_save_proc()
                # パケットを取得する
                msg = self.receive_udp_packet(1)
                if msg is None:
                    continue
                self.msgs_buffer.append(msg)
                if len(self.msgs_buffer) > self.msg_buf_size:
                    self.save_msgs()
            except KeyboardInterrupt:
                return
            except Exception as e:
                print(f"Error in server-save-file-main loop: {str(e)}")
        self._exit()

    def save_msgs(self) -> None:
        if len(self.msgs_buffer) != 0:
            self.save_msgs_q.put(self.msgs_buffer.copy())
            self.msgs_buffer.clear()

    def stop_loop(self) -> None:
        self.loop.put(STOP_COMMAND)

    def _exit(self) -> None:
        self.save_msgs()
        self.save_msgs_q.put(STOP_COMMAND)
        self.__exit__(None, None, None)


def save_proc(queue: Queue, save_path: str, edit_msg_func: callable) -> None:
    ensure_path_exists(save_path)
    while True:
        item = queue.get()
        if item == STOP_COMMAND:
            return
        save_str = "\n".join([edit_msg_func(msg.decode()) for msg in item]) + "\n"
        append_str_to_file(save_str, save_path)
