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
        obj =(obj*)
        path=(string)保存するパス
    @return:
        None
    pickleファイルとしてオブジェクトを保存する
    """
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_pickle(path: str) -> None:
    """
    @param:
        path=(string)読み込むパス
    @return:
        (obj *) 保存されていたオブジェクト
    pathに保存されていたオブジェクトをloadする
    """
    with open(path, "rb") as f:
        obj = pickle.load(f)
    return obj


def save_sentence(sentence: str, path: str, encoding="utf-8") -> None:
    """
    @param:
        sentence =(str)文字列データ
        path=(str)保存するパス
        encording=(str)encording
    @return:
        None
    文字列データをファイルに保存
    """
    with open(path, "w", encoding=encoding) as f:
        f.write(sentence)


def save_sentence_a(sentence: str, path: str, encoding="utf-8") -> None:
    """
    @param:
        sentence =(str)文字列データ
        path=(str)保存するパス
    @return:None
    文字列データを追記
    """
    if(not os.path.exists(path)):
        print(f'error: no such file {path}')
        return
    with open(path, "a", encoding=encoding) as f:
        f.write(sentence)


def __load_strls(path: str, encording="utf-8") -> list:
    """
    @param:
        path = string パス
    @return:
        list = [string]
        None
    pathに保存してある文字列をrowごとに取得
    pathが無かった場合=>return None
    """
    try:
        with open(path, "r", encoding=encording) as f:
            strls = f.readlines()
        return [row.replace("\n", "") for row in strls]
    except:
        return None


def load_sentence(path: str, encording="utf-8") -> str:
    """
    @param:
        path =string パス
    @return:
        string
        None
    txtファイルの中身を取り出す
    """
    sentence = ""
    strls = __load_strls(path, encording=encording)
    if strls is None:
        return
    for row in strls:
        sentence += row + "\n"
    return sentence


