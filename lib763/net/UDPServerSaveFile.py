from lib763.net.UDPServer import UDPServer
from lib763.fs.save_load import append_str_to_file
from lib763.fs.fs import ensure_path_exists
from lib763.multp.multp import start_process
from multiprocessing import Lock, Condition, Manager


class UdpServerSaveFile(UDPServer):
    def __init__(
        self, host: str, port: int, buffer_size: int, save_path: str, edit_msg_func
    ) -> None:
        """
        Initialize the UdpServerSaveFile.

        Args:
            host (str): The host address.
            port (int): The port number.
            buffer_size (int): The size of the buffer for receiving data.
            save_path (str): The path of the file to save the data.
        """
        super().__init__(host, port, buffer_size)
        self.FINISH_COMMAND = "\x02FINISH\x03"
        self.SAVE_COMMAND = "\x02SAVE\x03"
        self.save_path = save_path
        self.func = edit_msg_func

    def main(self) -> None:
        """
        The main loop for receiving UDP packets and saving them to a file.
        """
        decoded_msg_ls = []
        ensure_path_exists(self.save_path)
        saver = OrderedSaver(self.save_path, self.func)
        start_process(saver.main)
        try:
            while True:
                decoded_msg = self.receive_udp_packet().decode()
                if decoded_msg == self.FINISH_COMMAND:
                    self.__exit__(None, None, None)
                    saver.exit()
                    return
                elif decoded_msg == self.SAVE_COMMAND:
                    if len(decoded_msg_ls) != 0:
                        saver.append_data(decoded_msg_ls.copy())
                        decoded_msg_ls.clear()
                else:
                    decoded_msg_ls.append(decoded_msg)
        except Exception as e:
            print(f"Error in main loop: {str(e)}")


class OrderedSaver:
    def __init__(self, save_path: str, edit_msg_func: callable = None):
        """
        Initialize the OrderedSaver.

        Args:
            save_path (str): The path of the file to save the data.
        """
        self.save_path = save_path
        self.func = edit_msg_func
        self.dict_lock = Lock()
        self.data_dict = Manager().dict()
        self.condition = Condition()
        self.saver_loop = True
        self.current_key = 0
        self.current_save_key = 0

    def append_data(self, save_str_ls: list) -> None:
        """
        Append data to the internal dictionary.

        Args:
            save_str (str): The string to append.
        """
        with self.dict_lock:
            self.data_dict[self.current_key] = save_str_ls
            self.current_key += 1
            with self.condition:
                self.condition.notify()

    def main(self) -> None:
        """
        The main loop for saving data to a file.
        """
        while self.saver_loop:
            with self.condition:
                if len(self.data_dict.keys()) == 0:
                    self.condition.wait()
                with self.dict_lock:
                    save_str_ls = self.data_dict.pop(self.current_save_key)
                self.current_save_key += 1

            if self.func is None:
                if self.current_save_key != 1:
                    append_str_to_file("\n", self.save_path)
                append_str_to_file("\n".join(save_str_ls), self.save_path)
                continue

            save_str = "" if self.current_save_key == 1 else "\n"
            for save_str_line in save_str_ls:
                edited_str = self.func(save_str_line)
                if edited_str:
                    save_str += edited_str + "\n"
            append_str_to_file(save_str, self.save_path)

    def exit(self) -> None:
        """
        Exit the main loop.
        """
        self.saver_loop = False
