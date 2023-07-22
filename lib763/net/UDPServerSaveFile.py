from lib763.net.UDPServer import UDPServer
from lib763.fs.save_load import append_str_to_file
from lib763.fs.fs import ensure_path_exists
from lib763.multp.multp import start_process
from typing import Callable, List, Optional
import time


class UdpServerSaveFile(UDPServer):
    """
    A server for handling UDP packets and saving them to a file.

    Args:
        host: The host of the server.
        port: The port of the server.
        buffer_size: The maximum amount of data to be received at once.
        save_path: The path to the file where the data should be saved.
        edit_msg_func: A function to process the received data before saving.
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
        self.edit_msg_func = edit_msg_func
        self.loop = True
        self.decoded_messages = []
        self.state = SaveState()
        self.FINISH_COMMAND = "\x02FINISH\x03"
        self.SAVE_COMMAND = "\x02SAVE\x03"

    def main(self) -> None:
        """The main loop of the server, receiving and processing data."""
        ensure_path_exists(self.save_path)
        while self.loop:
            try:
                self.process_received_data()
            except Exception as e:
                print(f"Error in main loop: {str(e)}")

    def process_received_data(self) -> None:
        """Receives and processes data."""
        decoded_msg = self.receive_udp_packet().decode()
        if decoded_msg == self.FINISH_COMMAND:
            self.exit_this_server()
        elif decoded_msg == self.SAVE_COMMAND:
            self.save_received_data()
        else:
            self.decoded_messages.append(decoded_msg)

    def save_received_data(self) -> None:
        """Saves received data to a file."""
        if len(self.decoded_messages) != 0:
            start_process(
                save_thread,
                self.decoded_messages.copy(),
                self.state,
                self.save_path,
                self.edit_msg_func,
            )
            self.decoded_messages.clear()

    def exit_this_server(self) -> None:
        """Exits the server and finishes saving any remaining data."""
        if len(self.decoded_messages) != 0:
            self.save_received_data()
        self.__exit__(None, None, None)
        self.saver.stop()
        self.loop = False


class SaveState:
    """Tracks the state of saving operation."""

    def __init__(self):
        self.current_state = False
        self.current_ticket = 1
        self.issued_ticket = 0

    def get_state(self) -> bool:
        """Gets the current state."""
        return self.current_state

    def get_current_ticket(self) -> int:
        """Gets the current ticket."""
        return self.current_ticket

    def set_state(self, state_bool: bool) -> None:
        """Sets the current state."""
        self.current_state = state_bool

    def forward_current_ticket(self) -> None:
        """Advances the current ticket."""
        self.current_ticket += 1

    def issue_ticket(self) -> int:
        """Issues a new ticket and returns it."""
        self.issued_ticket += 1
        return self.issued_ticket


def save_thread(
    decoded_messages: List[str],
    save_state: SaveState,
    save_path: str,
    edit_msg_func: Callable,
) -> None:
    """A thread to save received messages."""
    ticket = save_state.issue_ticket()
    while not (
        (not save_state.get_state()) and (save_state.get_current_ticket() == ticket)
    ):
        time.sleep(0.2)
    save_state.set_state(True)
    save_data(decoded_messages, save_path, edit_msg_func)
    save_state.set_state(False)
    save_state.forward_current_ticket()


def save_data(
    decoded_messages: List[str], save_path: str, edit_msg_func: Callable
) -> None:
    """Saves the received data to a file."""
    save_str = ""
    for row in [edit_msg_func(row) for row in decoded_messages]:
        if row is not None:
            save_str += row + "\n"
    append_str_to_file(save_str, save_path)
