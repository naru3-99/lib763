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


def get_all_dir_path_in(target_dir: str) -> list:
    """
    @param:
        target_dir=(string)対象とするディレクトリ
    @return:
        [string]=対象ディレクトリ内のすべてのサブディレクトリ
    指定したディレクトリ内のすべてのサブディレクトリを取得
    """
    paths = glob.glob(target_dir + "/*/", recursive=True)
    return [path for path in paths if (os.path.isdir(path))]


def get_all_folder_name_in_nextdir(target_dir: str) -> list:
    """
    @param:
        target_dir =str 対象のフォルダのパス
    @return:
        list str = 対象のフォルダ直下のファイル名
    対象のフォルダ直下のファイル名を取得する
    """
    return [
        entry
        for entry in os.listdir(target_dir)
        if os.path.isfile(os.path.join(target_dir, entry))
    ]


def get_all_file_in_nextdir(target_dir: str) -> list:
    """
    @param:
        target_dir =str 対象のフォルダのパス
    @return:
        list str = 対象のフォルダ直下のフォルダ名
    対象のフォルダ直下のフォルダ名を取得する
    """

    return [
        entry
        for entry in os.listdir(target_dir)
        if os.path.isdir(os.path.join(target_dir, entry))
    ]


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
