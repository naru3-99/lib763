"""
2023/05/19
auther:naru
encoding=utf-8
"""

import glob
import os

from lib763.fs.save_load import *


def get_all_file_path_in(target_dir: str) -> list:
    """
    @param:
        target_dir=(string)対象とするディレクトリ
    @return:
        [string]=対象ディレクトリ内のすべてのパス
    指定したディレクトリ内のすべてのファイルのパスを取得
    """
    paths = glob.glob(target_dir + "/**/*", recursive=True)
    return [path for path in paths if (os.path.isfile(path))]


def is_same_extension(path: str, targ_extention: str) -> bool:
    """
    @param:
        path           =(str)ファイルのパス
        targ_extention =(str)拡張子
    @return:
        bool
    拡張子が一致するかどうかを返す
    """
    return get_file_extention(path) == targ_extention


def get_file_extention(path: str) -> str:
    """
    @param:
        path =(str)ファイルのパス
    @return:
        (str)ファイルの拡張子
    拡張子の文字列を取得する
    """
    extention_str = ""
    for i in path[::-1]:
        if i == ".":
            return extention_str[::-1]
        extention_str += i


def get_all_subdir_in(target_dir: str) -> list:
    """
    @param:
        target_dir=(string)対象とするディレクトリ
    @return:
        [string]=対象ディレクトリ内のすべてのサブディレクトリ
    指定したディレクトリ内のすべてのサブディレクトリを取得
    """
    paths = glob.glob(target_dir + "/*/", recursive=True)
    return [path for path in paths if (os.path.isdir(path))]


def get_dir_size(target_dir: str) -> int:
    """
    @param:
        target_dir=(string)対象とするディレクトリ
    @return:
        ディレクトリのサイズ
    指定したディレクトリのサイズを返す
    """
    total = 0
    with os.scandir(target_dir) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


def get_file_size(target_file: str) -> int:
    """
    @param:
        target_file=(string)対象とするファイル
    @return:
        ファイルのサイズ
    指定したファイルのサイズを返す
    """
    return os.path.getsize(target_file)
