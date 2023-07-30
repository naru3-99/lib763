from multiprocessing import Queue
from typing import Callable

from lib763.fs.fs import ensure_path_exists
from lib763.fs.save_load import append_str_to_file
from lib763.multp.multp import start_process
from lib763.net.UDPServer import UDPServer, socket

STOP_COMMAND = "\x02STOP\x03"


class UdpServerSaveFile(UDPServer):
    def __init__(
        self,
        host: str,
        port: int,
        udp_buffer_size: int,
        save_path: str,
        edit_msg_func: Callable,
        msg_buf_size: int,
    ) -> None:
        super().__init__(host, port, udp_buffer_size)
        self.loop = Queue()
        self.save_queue = Queue()
        self.msgs_buffer = []
        self.msg_buf_size = msg_buf_size
        start_process(save_proc, self.save_queue, save_path, edit_msg_func)

    def set_so_reuse(self):
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def main(self) -> None:
        while self.loop.empty():
            try:
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
            self.save_queue.put(self.msgs_buffer.copy())
            self.msgs_buffer.clear()

    def stop_loop(self) -> None:
        self.loop.put(STOP_COMMAND)

    def _exit(self) -> None:
        self.save_msgs()
        self.save_queue.put(STOP_COMMAND)
        self.__exit__(None, None, None)


def save_proc(queue: Queue, save_path: str, edit_msg_func: callable) -> None:
    ensure_path_exists(save_path)
    while True:
        item = queue.get()
        if item == STOP_COMMAND:
            return
        save_str = "\n".join([edit_msg_func(msg.decode()) for msg in item]) + "\n"
        append_str_to_file(save_str, save_path)
