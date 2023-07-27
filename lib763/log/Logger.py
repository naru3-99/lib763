from lib763.fs.save_load import save_str_to_file, load_str_from_file, append_str_to_file
import os
from multiprocessing import Lock


class Logger:
    """
    A singleton class that provides logging functionality to the application.
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

    def get_current_log(self):
        """
        Returns the current log from the log file.

        Returns:
            str: The current log from the log file.
        """
        with self.log_file_lock:
            current_log = load_str_from_file(self.log_file_path)
        return current_log
