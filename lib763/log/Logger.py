from lib763.fs.save_load import save_str_to_file, load_str_from_file, append_str_to_file
from lib763.fs.fs import rmrf
import os
from multiprocessing import Lock


class Logger:
    """
    Logger.get_instance() should be used to get the singleton instance of the Logger class.
    This logger is thread-safe.
    """

    __instance = None

    @classmethod
    def get_instance(cls, log_file_path):
        """
        Returns the singleton instance of the Logger class.

        Args:
            log_file_path (str): The path to the log file.

        Returns:
            Logger: The singleton instance of the Logger class.
        """
        if cls.__instance is None:
            cls.__instance = Logger(log_file_path)
        return cls.__instance

    def __init__(self, log_file_path):
        """
        Initializes the Logger class.

        Args:
            log_file_path (str): The path to the log file.
        """
        if Logger.__instance is not None:
            raise Exception("This class is a singleton!")
        self.log_file_path = log_file_path
        self.log_file_lock = Lock()

    def add_log(self, log_str):
        """
        Adds a log message to the log file.

        Args:
            log_str (str): The log message to add.
        """
        with self.log_file_lock:
            if os.path.exists(self.log_file_path):
                append_str_to_file(log_str + "\n", self.log_file_path)
                return
            save_str_to_file(log_str + "\n", self.log_file_path)

    def get_log(self):
        """
        Returns the current log from the log file.

        Returns:
            str: The current log from the log file.
        """
        with self.log_file_lock:
            current_log = load_str_from_file(self.log_file_path)
        return current_log

    def pop_logs_row(self, row):
        """完全に一致する行を削除する

        Args:
            row (str): 削除したい行
        """
        current_log = self.get_log()
        self.clear_log()
        self.add_log("\n".join([x for x in current_log.split("\n") if x != row]))

    def clear_log(self):
        """
        Clears the log file.
        """
        with self.log_file_lock:
            rmrf(self.log_file_path)
            save_str_to_file("", self.log_file_path)
