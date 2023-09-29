import multiprocessing as mp
import concurrent.futures
import time
from typing import Any, Callable, List, Union


def start_process(
    target: Callable[..., Any], *args: Union[List[Any], Any]
) -> mp.Process:
    """
    Starts a new process with the specified target function.

    Parameters:
    target (Callable): The function to be executed in the new process.
    *args (List[Any]): The list of arguments to be passed to the target function.

    Returns:
    Process: The new process object.
    """
    process = mp.Process(target=target, args=args)
    process.start()
    return process


def stop_process(process: mp.Process) -> None:
    """
    Terminates the specified process.

    Parameters:
    process (Process): The process object to be terminated.
    """
    if process.is_alive():
        process.terminate()


def parallel_process(func: Callable[..., Any], data_list: List[Any]) -> List[Any]:
    """
    Applies the specified function to every element in the list using concurrent.futures to parallelize the operation.

    Args:
        func (Callable[..., Any]): A function that takes one or more arguments and returns a value.
        data_list (List[Any]): A list of elements (or tuples of elements) to which the function will be applied.

    Returns:
        List[Any]: A list of results after applying the function to the elements of data_list.
    """
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(func, data_list)
    return list(results)


class EventHandler:
    def __init__(self) -> None:
        """
        Initializes a new Event object.
        """
        self._event = mp.Event()
        self.cur_event_type = mp.Value("i", -1)
        # dict[type] = handlers_list
        self.type_handlers_dict = {}

    def set_event(self, event_type: int = None):
        """
        Sets the event and calls the registered handlers.

        Parameters:
            event_type (int): The type of the event.
                              If specified, the current event type will be set to this value.
        """
        if event_type is not None and not isinstance(event_type, int):
            raise ValueError("event_type must be an integer or None")
        if not event_type is None:
            self.cur_event_type.value = event_type
            if not event_type in self.type_handlers_dict.keys():
                self.type_handlers_dict[event_type] = []
        self._event.set()
        self._call_handlers()

    def get_current_event_type(self):
        """
        Returns the current event type.
        """
        return self.cur_event_type.value

    def clear_event(self, event_type: int = None):
        """
        Clears the event and resets the current event type.
        Parameters:
        event_type (int): The type of the event.
                          If specified, the current event type will be set to this value.
        """
        if event_type is not None and not isinstance(event_type, int):
            raise ValueError("event_type must be an integer or None")

        if not event_type == None:
            if event_type != self.cur_event_type.value:
                print(f"current event is {self.cur_event_type.value}, not {event_type}")
                return
        self._event.clear()
        self.cur_event_type.value = -1

    def wait(self, event_type: int = None, timeout: float = None):
        """
        Waits for the event to be set.

        Parameters:
            event_type (int): The type of the event to wait for. If None, waits for any event to be set.
            timeout (float): The maximum time to wait for the event to be set.
        Returns:
            bool: True if the event was set, False otherwise.
        """
        if event_type is not None and not isinstance(event_type, int):
            raise ValueError("event_type must be an integer or None")

        if event_type is None:
            return self._event.wait(timeout)

        start_time = time.time()

        while True:
            if not timeout is None:
                if time.time() - start_time > timeout:
                    return False
            if self.get_current_event_type() == event_type:
                return True
            time.sleep(0.2)

    def register_handler(self, event_type: int, handler: Callable):
        """
        Registers a new handler for the specified event type.

        Parameters:
            event_type (int): The type of the event.
            handler (Callable): The handler function to be called when the event is set.
        """
        if event_type is not None and not isinstance(event_type, int):
            raise ValueError("event_type must be an integer or None")

        if not callable(handler):
            raise TypeError("handler must be Callable")

        if not event_type is None:
            if not event_type in self.type_handlers_dict.keys():
                self.type_handlers_dict[event_type] = []
        self.type_handlers_dict[event_type].append(handler)

    def _call_handlers(self):
        """
        Calls all registered handlers for the current event type.
        """
        for func in self.type_handlers_dict[self.cur_event_type.value]:
            func()
