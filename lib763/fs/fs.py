"""
2023/05/19
auther: naru
encoding=utf-8
"""

import os
import shutil
from lib763.fs.path import *
from lib763.fs.save_load import *


def mkdir(target_dir: str, folder_name: str) -> None:
    """
    @param:
        target_dir: (str) 対象とするディレクトリ
        folder_name: (str) 作成するフォルダの名前
    @return:
        None
    フォルダを作成します。
    """
    if not os.path.exists(target_dir) or os.path.exists(
        os.path.join(target_dir, folder_name)
    ):
        return
    os.mkdir(os.path.join(target_dir, folder_name))


def create_serial_dir(target_dir: str) -> None:
    """
    @param:
        target_dir: (str) 対象とするディレクトリ
    @return:
        None
    1, 2, ... と連番のディレクトリを作成します。
    """
    mkdir(target_dir, str(get_len_of_dir_in(target_dir) + 1))


def create_serial_file(target_dir: str, extension: str) -> None:
    """
    @param:
        target_dir: (str) 対象とするディレクトリ
        extension: (str) 拡張子
    @return:
        None
    1, 2, ... と連番のファイルを作成します。
    """
    num = get_len_of_file_in(target_dir)
    save_sentence("", os.path.join(target_dir, f"{num}.{extension}"))


def get_len_of_dir_in(target_dir: str) -> int:
    """
    @param:
        target_dir: (str) 対象とするディレクトリ
    @return:
        int
    ディレクトリ内のサブディレクトリの数を返します。
    """
    return len(get_all_dir_path_in(target_dir))


def get_len_of_file_in(target_dir: str) -> int:
    """
    @param:
        target_dir: (str) 対象とするディレクトリ
    @return:
        int
    ディレクトリ内のファイルの数を返します。
    """
    return len(get_all_file_path_in(target_dir))


def rmrf(path: str) -> None:
    """
    @param:
        path: (str) 削除するパス
    @return:
        None
    ディレクトリやファイルを再帰的に削除します。rm -rfコマンドのような動作です。
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
        load_path: (str) コピー元のパス
        save_path: (str) コピー先のパス
    @return:
        None
    ファイルをコピーします。
    """
    return save_sentence(load_sentence(load_path), save_path)
