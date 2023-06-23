"""
2023/05/19
auther: naru
encoding=utf-8
"""

import os
import shutil
import tarfile
import zipfile

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


def create_tar_archive(directory_path: str, archive_name: str) -> None:
    """
    @param:
        directory_path: (str) 保存するディレクトリ
        archive_name  : (str) アーカイブファイルの名前
    @return:
        None
    tarによる圧縮を行う。
    create_tar_archive('/path/to/directory', 'archive.tar')
    """
    with tarfile.open(archive_name, "w") as tar:
        tar.add(directory_path, arcname="directory")


def extract_tar_archive(extract_path: str, archive_name: str) -> None:
    """
    @param:
        extract_path: (str) 解凍するパス
        archive_name  : (str) アーカイブファイルの名前
    @return:
        None
    tarによる解凍を行う。
    extract_tar_archive("/path/to/extract","archive.tar")
    """
    with tarfile.open(archive_name, "r") as tar:
        tar.extractall(extract_path)


def create_zip_archive(directory_path, archive_name):
    """
    @param:
        directory_path: (str) 保存するディレクトリ
        archive_name  : (str) アーカイブファイルの名前
    @return:
        None
    zipによる圧縮を行う。
    create_zip_archive("/path/to/directory", "archive")
    """
    shutil.make_archive(archive_name, "zip", directory_path)


def extract_zip_archive(extract_path, archive_name):
    """
    @param:
        extract_path: (str) 解凍するパス
        archive_name  : (str) アーカイブファイルの名前
    @return:
        None
    zipによる解凍を行う。
    extract_zip_archive("archive.zip", "/path/to/extract")
    """
    with zipfile.ZipFile(archive_name, "r") as zip_ref:
        zip_ref.extractall(extract_path)


def rename(target_dir: str, before: str, after: str, force=False) -> bool:
    """
    ファイルをリネームします。
    @Args:
        target_dir (str): ファイルが存在するディレクトリのパス
        before (str): リネーム前のファイル名
        after (str): リネーム後のファイル名
        force (bool, optional): 同名のファイルが存在する場合に上書きするかどうかを指定します。デフォルトは False です。
    @Returns:
        bool: リネームが成功した場合は True、失敗した場合は False を返します。
    """
    if not os.path.exists(target_dir):
        print(f"No such directory: {target_dir}")
        return False
    before_path = os.path.join(target_dir, before)
    if not os.path.isfile(before_path):
        print(f"No such file: {before_path}")
        return False
    after_path = os.path.join(target_dir, after)
    if not force:
        if os.path.exists(after_path):
            print(f"File already exists: {after_path}")
            return False
    try:
        os.rename(before_path, after_path)
        return True
    except Exception as e:
        print(f"Error renaming file: {e}")
        return False
