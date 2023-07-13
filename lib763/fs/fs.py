import os
import shutil
import zipfile
from typing import Union
from lib763.fs.path import get_all_file_names_in, get_dir_names_in
from lib763.fs.save_load import load_str_from_file, save_str_to_file


def mkdir(target_dir: str, folder_name: str) -> Union[str, None]:
    """
    指定したパスに新しいディレクトリを作成します。

    Args:
        target_dir (str): 新しいディレクトリを作成する親ディレクトリのパス
        folder_name (str): 作成する新しいディレクトリの名前

    Returns:
        str: 成功した場合には作成したディレクトリのパス
        None: 親ディレクトリが存在しない場合や、作成しようとしたディレクトリがすでに存在する場合
    """
    if not os.path.exists(target_dir) or os.path.exists(
        os.path.join(target_dir, folder_name)
    ):
        return None

    new_folder_path = os.path.join(target_dir, folder_name)
    os.mkdir(new_folder_path)
    return new_folder_path


def ensure_path_exists(path: str) -> bool:
    """Ensure the given path exists in the file system.

    This function creates the directories and file if they do not exist.
    If the path points to a directory, it will be created. If the path points to
    a file, the directories will be created and an empty file will be generated.

    Args:
        path (str): The file or directory path that should be ensured to exist.

    Returns:
        bool: True if the path was successfully created, False if the path already exists.

    Raises:
        OSError: If there is a failure in directory or file creation due to a system-related error.
    """
    if path == "":
        return False
    if os.path.exists(path):
        return False

    if path.endswith("/"):
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except OSError:
            raise
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            pass
    except OSError:
        raise
    return True


def create_serial_dir(target_dir: str) -> Union[str, None]:
    """
    指定したパスに連番のディレクトリを作成します。

    Args:
        target_dir (str): 新しいディレクトリを作成する親ディレクトリのパス

    Returns:
        str: 成功した場合には作成したディレクトリのパス
        None: 親ディレクトリが存在しない場合や、作成しようとしたディレクトリがすでに存在する場合
    """
    return mkdir(target_dir, str(len(get_dir_names_in(target_dir)) + 1))


def create_serial_file(target_dir: str, extension: str) -> Union[str, None]:
    """
    指定したパスに連番のファイルを作成します。

    Args:
        target_dir (str): 新しいファイルを作成する親ディレクトリのパス
        extension (str): 作成する新しいファイルの拡張子

    Returns:
        str: 成功した場合には作成したファイルの名前
        None: ファイルの作成に失敗した場合
    """
    file_name = f"{get_all_file_names_in(target_dir)}.{extension}"
    file_path = os.path.join(target_dir, file_name)
    try:
        save_str_to_file("", file_path)
        return file_name
    except:
        return None


def rmrf(path: str) -> None:
    """ディレクトリやファイルを再帰的に削除します。

    Args:
        path (str): 削除するパス
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
    """ファイルをコピーします。

    Args:
        load_path (str): コピー元のパス
        save_path (str): コピー先のパス
    """
    return save_str_to_file(load_str_from_file(load_path), save_path)


def rename(target_dir: str, before: str, after: str, force=False) -> bool:
    """ファイルをリネームします。

    Args:
        target_dir (str): ファイルが存在するディレクトリのパス
        before (str): リネーム前のファイル名
        after (str): リネーム後のファイル名
        force (bool, optional): 同名のファイルが存在する場合に上書きするかどうかを指定します。デフォルトは False です。

    Returns:
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
    if os.path.exists(after_path):
        if not force:
            print(f"File already exists: {after_path}")
            return False
    try:
        os.rename(before_path, after_path)
        return True
    except Exception as e:
        print(f"Error renaming file: {e}")
        return False


def move_file(src_path: str, dst_path: str) -> bool:
    """Move a file from src_path to dst_path.

    This function moves a file from the source path to the destination path.
    If the destination directory doesn't exist, it is created.
    The function will print out information about the operation.
    In case of an exception, the error message is printed.

    Args:
        src_path (str): The source file path.
        dst_path (str): The destination file path.

    Returns:
        bool: True if the file was successfully moved, False otherwise.
    """

    if not os.path.isfile(src_path):
        print(f"No such file: '{src_path}'")
        return False

    dst_dir = os.path.dirname(dst_path)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    try:
        shutil.move(src_path, dst_path)
        print(f"File moved: '{src_path}' to '{dst_path}'")
        return True
    except Exception as e:
        print(f"Can't move file: '{src_path}' to '{dst_path}'. Reason: {e}")
        return False


def create_zip_archive(directory_path, archive_name):
    """zipによる圧縮を行います。

    Args:
        directory_path (str): 保存するディレクトリ
        archive_name (str): アーカイブファイルの名前
    """
    shutil.make_archive(archive_name, "zip", directory_path)


def extract_zip_archive(extract_path, archive_name):
    """zipによる解凍を行います。

    Args:
        extract_path (str): 解凍するパス
        archive_name (str): アーカイブファイルの名前
    """
    with zipfile.ZipFile(archive_name, "r") as zip_ref:
        zip_ref.extractall(extract_path)
