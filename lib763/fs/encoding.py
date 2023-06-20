"""
2023/05/19
auther: naru
encoding=utf-8
"""

import chardet


def get_file_encoding(path: str) -> str:
    """
    @param:
        path: (str) 読み込むファイルのパス
    @return:
        str: ファイルのエンコードを予測した結果
    パスで指定されたファイルのエンコードを予測します。
    """
    with open(path, "rb") as f:
        result = chardet.detect(f.read())
    return result["encoding"]


def change_encoding(sentence: str, before: str, after: str) -> str:
    """
    @param:
        sentence: (str) エンコードを変更する文字列
        before: (str) 変更前のエンコーディング
        after: (str) 変更後のエンコーディング
    @return:
        str: エンコーディングが変更された文字列
    文字列のエンコーディングを変更します。
    """
    return sentence.encode(before).decode(after)
