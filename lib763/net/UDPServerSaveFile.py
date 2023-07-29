from multiprocessing import Queue
from typing import Callable, List
import time
import sys

from lib763.fs.fs import ensure_path_exists
from lib763.fs.save_load import append_str_to_file
from lib763.multp.multp import start_process

from lib763.net.UDPServer import UDPServer
from lib763.net.CONST import SAVE_COMMAND, FINISH_COMMAND, STOP_COMMAND


class UdpServerSaveFile(UDPServer):
    def __init__(
        self,
        host: str,
        port: int,
        buffer_size: int,
        save_path: str,
        edit_msg_func: Callable,
    ) -> None:
        """
        A UDP server that saves incoming messages to a file.

        Args:
        - host (str): The host address to bind the server to.
        - port (int): The port number to bind the server to.
        - buffer_size (int): The maximum size of the incoming message buffer.
        - save_path (str): The path to the file where the messages will be saved.
        - edit_msg_func (Callable): A function to edit the incoming messages before saving them.
        """
        super().__init__(host, port, buffer_size)
        self.save_path = save_path
        self.edit_msg_func = edit_msg_func
        self.loop_queue = Queue()
        self.save_queue = Queue()
        self.decoded_messages = []

    def stop_loop(self) -> None:
        """
        Stops the main loop of the server.
        """
        self.loop_queue.put(STOP_COMMAND)

    def main(self) -> None:
        """
        The main loop of the server.
        """
        ensure_path_exists(self.save_path)
        start_process(save_proc, self.save_queue, self.save_path)
        while self.loop_queue.empty():
            try:
                self.receive_and_deal()
            except KeyboardInterrupt:
                return
            except Exception as e:
                print(f"Error in server-save-file-main loop: {str(e)}")
        self._exit()

    def receive_and_deal(self) -> None:
        """
        Receives an incoming message and deals with it accordingly.
        """
        decoded_msg = self.receive_udp_packet().decode()
        if decoded_msg == FINISH_COMMAND:
            self.stop_loop()
        elif decoded_msg == SAVE_COMMAND:
            self.save_msgs()
        else:
            edited_msg = self.edit_msg_func(decoded_msg)
            self.decoded_messages.append(edited_msg)

    def save_msgs(self) -> None:
        """
        Saves the incoming messages to the file.
        """
        if len(self.decoded_messages) != 0:
            self.save_queue.put(self.decoded_messages.copy())
            self.decoded_messages.clear()

    def _exit(self) -> None:
        """
        Exits the server.
        """
        if len(self.decoded_messages) != 0:
            self.save_msgs()
        self.save_queue.put(STOP_COMMAND)
        self.__exit__(None, None, None)
        sys.exit()


def save_proc(queue: Queue, save_path: str) -> None:
    """
    A process that saves the incoming messages to the file.

    Args:
    - queue (Queue): The queue containing the incoming messages.
    - save_path (str): The path to the file where the messages will be saved.
    """
    while True:
        item = queue.get()
        if item == STOP_COMMAND:
            sys.exit()
        append_str_to_file("\n".join(item) + "\n", save_path)
