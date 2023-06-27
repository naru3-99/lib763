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
        target_dir: (str) 対象とするディレクトリ
    @return:
        [str]: 対象ディレクトリ内のすべてのファイルのパス
    指定したディレクトリ内のすべてのファイルのパスを取得します。
    """
    return [
        path.replace("\\", "/")
        for path in glob.glob(target_dir + "/**/*", recursive=True)
        if (os.path.isfile(path))
    ]


def get_all_dir_path_in(target_dir: str) -> list:
    """
    @param:
        target_dir: (str) 対象とするディレクトリ
    @return:
        [str]: 対象ディレクトリ内のすべてのサブディレクトリ
    指定したディレクトリ内のすべてのサブディレクトリのパスを取得します。
    """
    return [
        path.replace("\\", "/")
        for path in glob.glob(target_dir + "/*/", recursive=True)
        if (os.path.isdir(path))
    ]


def get_all_folder_name_in_nextdir(target_dir: str) -> list:
    """
    @param:
        target_dir: (str) 対象のフォルダのパス
    @return:
        [str]: 対象のフォルダ直下のフォルダ名
    対象のフォルダ直下のフォルダ名を取得します。
    """
    return [
        entry
        for entry in os.listdir(target_dir)
        if os.path.isdir(os.path.join(target_dir, entry))
    ]


def get_all_file_in_nextdir(target_dir: str) -> list:
    """
    @param:
        target_dir: (str) 対象のフォルダのパス
    @return:
        [str]: 対象のフォルダ直下のファイル名
    対象のフォルダ直下のファイル名を取得します。
    """
    return [
        entry
        for entry in os.listdir(target_dir)
        if os.path.isfile(os.path.join(target_dir, entry))
    ]


def get_file_extension(path: str) -> str:
    """
    @param:
        path: (str) ファイルのパス
    @return:
        str: ファイルの拡張子
    ファイルの拡張子の文字列を取得します。
    """
    extension_str = ""
    for i in path[::-1]:
        if i == ".":
            return extension_str[::-1]
        extension_str += i


def get_file_name(path: str) -> str:
    """
    @param:
        path: (str) ファイルのパス
    @return:
        str: ファイルの名前
    ファイル名の文字列を取得します。
    """
    return os.path.basename(path)


def get_parent_directory(file_path: str) -> str:
    """
    ファイルのパスから直下のディレクトリを取得します。
    @Args:
        file_path (str): ファイルのパス
    @Returns:
        str: ファイルの存在する直下のディレクトリのパス
    """
    return os.path.dirname(file_path)


def get_dir_size(target_dir: str) -> int:
    """
    @param:
        target_dir: (str) 対象とするディレクトリ
    @return:
        int: ディレクトリのサイズ
    指定したディレクトリのサイズを返します。
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
        target_file: (str) 対象とするファイル
    @return:
        int: ファイルのサイズ
    指定したファイルのサイズを返します。
    """
    return os.path.getsize(target_file)
