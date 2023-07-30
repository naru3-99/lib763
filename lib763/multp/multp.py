from multiprocessing import Process, Pool, cpu_count
from typing import Any, Callable, List, Union


def start_process(target: Callable[..., Any], *args: Union[List[Any], Any]) -> Process:
    """
    指定したターゲット関数を新しいプロセスで開始する。

    Parameters:
    target (Callable): 新しいプロセスで実行する関数
    *args (List[Any]): ターゲット関数に渡す引数リスト

    Returns:
    Process: 新しいプロセスオブジェクト
    """
    process = Process(target=target, args=args)
    process.start()
    return process


def stop_process(process: Process) -> None:
    """
    指定したプロセスを終了する。

    Parameters:
    process (Process): 終了させるプロセスオブジェクト
    """
    if process.is_alive():
        process.terminate()


def parallel_process(func: Callable[[Any], Any], data_list: List[Any]) -> List[Any]:
    """
    Given a function and a list, applies the function to every element in the list using
    multiprocessing to parallelize the operation and return the result list.

    Args:
        func (Callable[[Any], Any]): A function that takes a single argument and returns a value.
        data_list (List[Any]): A list of elements to which the function will be applied.

    Returns:
        List[Any]: A list of results after applying the function to the elements of data_list.

    """
    pool = Pool(cpu_count())
    result = pool.map(func, data_list)

    pool.close()
    pool.join()
    return result
