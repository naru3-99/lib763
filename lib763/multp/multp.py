from multiprocessing import Process
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
    process.terminate()
