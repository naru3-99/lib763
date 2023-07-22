from lib763.net.UDPServer import UDPServer
from lib763.fs.save_load import append_str_to_file
from lib763.fs.fs import ensure_path_exists
from lib763.multp.multp import start_process
from multiprocessing import Lock, Condition, Manager
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
        self.func = edit_msg_func
        self.saver = OrderedSaver(self.save_path, self.func)
        self.FINISH_COMMAND = "\x02FINISH\x03"
        self.SAVE_COMMAND = "\x02SAVE\x03"
        self.loop = True
        self.decoded_msg_ls = []

    def main(self) -> None:
        """The main loop of the server, receiving and processing data."""
        ensure_path_exists(self.save_path)
        start_process(self.saver.main)
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
        self.saver.exit()
        self.loop = False


class OrderedSaver:
    """A helper class for saving data in a certain order.

    Args:
        save_path (str): The path to the file where the data should be saved.
        edit_msg_func (Callable): A function to process the data before saving.
    """

    def __init__(self, save_path: str, edit_msg_func: Callable = None):
        self.save_path = save_path
        self.func = edit_msg_func
        self.dict_lock = Lock()
        self.data_dict = Manager().dict()
        self.condition = Condition()
        self.loop = True
        self.current_key = 0
        self.current_save_key = 0

    def append_data(self, save_str_ls: List[str]) -> None:
        """Appends data to the save list.

        Args:
            save_str_ls (List[str]): The data to be saved.
        """
        with self.dict_lock:
            self.data_dict[self.current_key] = save_str_ls
            self.current_key += 1
            with self.condition:
                self.condition.notify()

    def main(self) -> None:
        """The main loop of the saver, processing and saving data."""
        while self.loop or self.current_key != self.current_save_key:
            with self.condition:
                if len(self.data_dict.keys()) == 0:
                    self.condition.wait()
                with self.dict_lock:
                    save_str_ls = self.data_dict.pop(self.current_save_key)

            if self.func is None:
                append_str_to_file("\n".join(save_str_ls) + "\n", self.save_path)
                self.current_save_key += 1
                continue

            save_str = ""
            for save_str_line in save_str_ls:
                edited_str = self.func(save_str_line)
                if edited_str:
                    save_str += edited_str + "\n"
            append_str_to_file(save_str + "\n", self.save_path)
            self.current_save_key += 1

    def exit(self) -> None:
        """Exits the saver, stopping any further saving."""
        self.loop = False
