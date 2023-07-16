from lib763.net.UDPServer import UDPServer
from lib763.fs.save_load import append_str_to_file
from multiprocessing import Process, Lock, Condition


class UdpServerSaveFile(UDPServer):
    def __init__(self, host: str, port: int, buffer_size: int, save_path) -> None:
        super().__init__(host, port, buffer_size)
        self.FINISH_COMMAND = "\x02FINISH\x03"
        self.SAVE_COMMAND = "\x02SAVE\x03"
        self.saver = OrderedSaver(save_path)

    def edit_save_str(self, recieved_str: str) -> str:
        raise NotImplementedError("This method must be implemented by subclasses")

    def main(self) -> None:
        decoded_msg_ls = []
        Process(target=self.saver.main).start()
        try:
            while True:
                decoded_msg = self.receive_udp_packet().decode()
                if decoded_msg == self.FINISH_COMMAND:
                    self.__exit__(None, None, None)
                    self.saver.exit()
                    return
                elif decoded_msg == self.SAVE_COMMAND:
                    self.saver.append_data(
                        "\n".join([self.edit_save_str(msg) for msg in decoded_msg_ls])
                    )
                    decoded_msg_ls.clear()
                else:
                    decoded_msg_ls.append(decoded_msg)
        except Exception as e:
            print(f"Error in main loop: {str(e)}")


class OrderedSaver:
    def __init__(self, save_path):
        self.save_path = save_path
        self.dict_lock = Lock()
        self.data_dict = {}
        self.current_key = 0
        self.saver_loop = True
        self.condition = Condition(self.dict_lock)

    def append_data(self, save_str):
        with self.condition:
            self.data_dict[self.current_key] = save_str
            self.current_key += 1
            self.condition.notify()

    def main(self):
        while self.saver_loop:
            with self.condition:
                if len(self.data_dict.keys()) == 0:
                    self.condition.wait()
                save_str = self.data_dict.pop(min(self.data_dict.keys()))
                append_str_to_file(save_str, self.save_path)

    def exit(self):
        self.saver_loop = False
