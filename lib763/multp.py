import multiprocessing as mp
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


def parallel_process(func: Callable[[Any], Any], data_list: List[Any]) -> List[Any]:
    """
    Applies the specified function to every element in the list using multiprocessing to parallelize the operation.

    Args:
        func (Callable[[Any], Any]): A function that takes a single argument and returns a value.
        data_list (List[Any]): A list of elements to which the function will be applied.

    Returns:
        List[Any]: A list of results after applying the function to the elements of data_list.

    """
    pool = mp.Pool(mp.cpu_count())
    result = pool.map(func, data_list)

    pool.close()
    pool.join()
    return result


class Event:
    def __init__(self) -> None:
        """
        Initializes a new Event object.
        """
        self._event = mp.Event()
        self.cur_event_type = None
        # dict[type] = handlers_list
        self.type_handlers_dict = {}

    def set_event(self, event_type: str = None):
        """
        Sets the event and calls the registered handlers.

        Parameters:
        event_type (str): The type of the event. If specified, the current event type will be set to this value.
        """
        if not event_type is None:
            self.cur_event_type = event_type
            if not event_type in self.type_handlers_dict.keys():
                self.type_handlers_dict[event_type] = []
        self._event.set()
        self._call_handlers()

    def clear_event(self):
        """
        Clears the event and resets the current event type.
        """
        self._event.clear()
        self.cur_event_type = None

    def wait(self, timeout=None):
        """
        Waits for the event to be set.

        Parameters:
        timeout (float): The maximum time to wait for the event to be set.

        Returns:
        bool: True if the event was set, False otherwise.
        """
        return self._event.wait(timeout)

    def register_handler(self, event_type, handler):
        """
        Registers a new handler for the specified event type.

        Parameters:
        event_type (str): The type of the event.
        handler (Callable): The handler function to be called when the event is set.
        """
        if not event_type is None:
            if not event_type in self.type_handlers_dict.keys():
                self.type_handlers_dict[event_type] = []
        self.type_handlers_dict[event_type].append(handler)

    def _call_handlers(self):
        """
        Calls all registered handlers for the current event type.
        """
        for func in self.type_handlers_dict[self.cur_event_type]:
            func()
