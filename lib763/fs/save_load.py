import pickle
import os


def save_object_to_file(obj: object, path: str) -> None:
    """オブジェクトをpickleファイルとして保存します。

    Args:
        obj: 保存するオブジェクト
        path: 保存するパス
    """
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_object_from_file(path: str) -> object:
    """指定したパスのpickleファイルからオブジェクトを読み込みます。

    Args:
        path: 読み込むパス

    Returns:
        保存されていたオブジェクト

    Raises:
        FileNotFoundError: 指定したパスが存在しない場合
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")
    with open(path, "rb") as f:
        obj = pickle.load(f)
    return obj


def save_str_to_file(sentence: str, path: str, encoding="utf-8") -> None:
    """文字列データを指定したパスにテキストファイルとして保存します。

    Args:
        sentence: 文字列データ
        path: 保存するパス
        encoding: エンコーディング
    """
    with open(path, "w", encoding=encoding) as f:
        f.write(sentence)


def append_str_to_file(sentence: str, path: str, encoding="utf-8") -> None:
    """文字列データを指定したパスに追記します。

    Args:
        sentence: 文字列データ
        path: 保存するパス
        encoding: エンコーディング

    Raises:
        FileNotFoundError: 指定したパスが存在しない場合
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")
    with open(path, "a", encoding=encoding) as f:
        f.write(sentence)


def load_str_from_file(path: str, encoding="utf-8") -> str:
    """指定したパスのテキストファイルの内容を取得します。

    Args:
        path: パス

    Returns:
        テキストファイルの内容

    Raises:
        FileNotFoundError: 指定したパスが存在しない場合
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")
    with open(path, "r", encoding=encoding) as f:
        lines = [line.rstrip() for line in f]
    return "\n".join(lines)
