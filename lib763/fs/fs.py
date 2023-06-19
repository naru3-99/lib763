"""
2023/05/19
auther:naru
encoding=utf-8
"""

import os
import shutil
from lib763.fs.path import *
from lib763.fs.save_load import *


def mkdir(target_dir: str, folder_name: str) -> None:
    """
    @param:
        target_dir=(string)対象とするディレクトリ
        folder_name=(string)作成するフォルダの名前
    @return:
        none
    フォルダを作成する。
    """
    if not os.path.exists(target_dir) or os.path.exists(
        os.path.join(target_dir, folder_name)
    ):
        return
    os.mkdir(os.path.join(target_dir, folder_name))


def create_serial_dir(target_dir: str) -> None:
    """
    @param:
        target_dir=(string)対象とするディレクトリ
    @return:
        none
    1,2,...と言った連番のディレクトリを作成する
    """
    mkdir(target_dir, str(get_len_of_dir_in(target_dir) + 1))


def create_serial_file(target_dir: str, extention: str) -> None:
    """
    @param:
        target_dir=(string)対象とするディレクトリ
        extention =(string)拡張子
    @return:
        none
    1,2,...と言った連番のファイルを作成する
    """
    num = get_len_of_file_in(target_dir)
    save_sentence("", os.path.join(target_dir, f"{num}.{extention}"))


def get_len_of_dir_in(target_dir: str) -> int:
    """
    @param:
        target_dir=(string)対象とするディレクトリ
    @return:
        int
    ディレクトリの中にあるディレクトリの数を返す
    """
    return len(get_all_dir_path_in(target_dir))


def get_len_of_file_in(target_dir: str) -> int:
    """
    @param:
        target_dir=(string)対象とするディレクトリ
    @return:
        int
    ディレクトリの中にあるファイルの数を返す
    """
    return len(get_all_file_path_in(target_dir))


def rmrf(path: str) -> None:
    """
    @param:
        path: 削除するパス
    @return:
        int
    ディレクトリ、ファイル構わずすべて削除
    bashのrm -rfコマンドみたいに
    """
    if os.path.isfile(path):
        try:
            os.remove(path)
        except FileNotFoundError:
            print("指定したファイルが見つかりません。")
        except PermissionError:
            print("ファイルの削除権限がありません。")
        except Exception as e:
            print(f"ファイルの削除中にエラーが発生しました: {e}")
    else:
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            print("指定したディレクトリが見つかりません。")
        except PermissionError:
            print("ディレクトリの削除権限がありません。")
        except Exception as e:
            print(f"ディレクトリの削除中にエラーが発生しました: {e}")

def copy_file(load_path: str, save_path: str) -> None:
    """
    @param:
        load_path=(str)ロードするパス
        save_path=(str)セーブするパス
    @return:
        None
    ファイルをコピーする
    """
    return save_sentence(load_sentence(load_path), save_path)
