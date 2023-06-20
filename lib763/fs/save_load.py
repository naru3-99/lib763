"""
2023/05/19
auther:naru
encoding=utf-8
"""

import pickle
import os


def save_pickle(obj: object, path: str) -> None:
    """
    @param:
        obj: (object) 保存するオブジェクト
        path: (str) 保存するパス
    @return:
        None
    オブジェクトをpickleファイルとして保存します。
    """
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_pickle(path: str) -> object:
    """
    @param:
        path: (str) 読み込むパス
    @return:
        object: 保存されていたオブジェクト
    指定したパスのpickleファイルからオブジェクトを読み込みます。
    """
    with open(path, "rb") as f:
        obj = pickle.load(f)
    return obj


def save_sentence(sentence: str, path: str, encoding="utf-8") -> None:
    """
    @param:
        sentence: (str) 文字列データ
        path: (str) 保存するパス
        encoding: (str) エンコーディング
    @return:
        None
    文字列データを指定したパスにテキストファイルとして保存します。
    """
    with open(path, "w", encoding=encoding) as f:
        f.write(sentence)


def save_sentence_a(sentence: str, path: str, encoding="utf-8") -> None:
    """
    @param:
        sentence: (str) 文字列データ
        path: (str) 保存するパス
        encoding: (str) エンコーディング
    @return:
        None
    文字列データを指定したパスに追記します。
    """
    if not os.path.exists(path):
        print(f"error: no such file {path}")
        return
    with open(path, "a", encoding=encoding) as f:
        f.write(sentence)


def __load_strls(path: str, encoding="utf-8") -> list:
    """
    @param:
        path: (str) パス
    @return:
        list: [str]
        None
    指定したパスに保存された文字列を行ごとに取得します。
    パスが存在しない場合はNoneを返します。
    """
    try:
        with open(path, "r", encoding=encoding) as f:
            strls = f.readlines()
        return [row.replace("\n", "") for row in strls]
    except:
        return None


def load_sentence(path: str, encoding="utf-8") -> str:
    """
    @param:
        path: (str) パス
    @return:
        str
        None
    指定したパスのテキストファイルの内容を取得します。
    """
    sentence = ""
    strls = __load_strls(path, encoding=encoding)
    if strls is None:
        return
    for row in strls:
        sentence += row + "\n"
    return sentence
