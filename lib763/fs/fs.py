import os
import shutil
import tarfile
import zipfile
from lib763.fs.path import get_all_dir_path_in, get_all_file_path_in
from lib763.fs.save_load import load_sentence, save_sentence


def mkdir(target_dir: str, folder_name: str) -> str | None:
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


def create_serial_dir(target_dir: str) -> str | None:
    """
    指定したパスに連番のディレクトリを作成します。

    Args:
        target_dir (str): 新しいディレクトリを作成する親ディレクトリのパス

    Returns:
        str: 成功した場合には作成したディレクトリのパス
        None: 親ディレクトリが存在しない場合や、作成しようとしたディレクトリがすでに存在する場合
    """
    return mkdir(target_dir, str(get_len_of_dir_in(target_dir) + 1))


def create_serial_file(target_dir: str, extension: str) -> str | None:
    """
    指定したパスに連番のファイルを作成します。

    Args:
        target_dir (str): 新しいファイルを作成する親ディレクトリのパス
        extension (str): 作成する新しいファイルの拡張子

    Returns:
        str: 成功した場合には作成したファイルの名前
        None: ファイルの作成に失敗した場合
    """
    file_name = f"{get_len_of_file_in(target_dir)}.{extension}"
    file_path = os.path.join(target_dir, file_name)
    try:
        save_sentence("", file_path)
        return file_name
    except:
        return None


def get_len_of_dir_in(target_dir: str) -> int:
    """ディレクトリ内のサブディレクトリの数を返します。

    Args:
        target_dir (str): 対象とするディレクトリ

    Returns:
        int: ディレクトリ内のサブディレクトリの数
    """
    return len(get_all_dir_path_in(target_dir))


def get_len_of_file_in(target_dir: str) -> int:
    """ディレクトリ内のファイルの数を返します。

    Args:
        target_dir (str): 対象とするディレクトリ

    Returns:
        int: ディレクトリ内のファイルの数
    """
    return len(get_all_file_path_in(target_dir))


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
    return save_sentence(load_sentence(load_path), save_path)


def create_tar_archive(directory_path: str, archive_name: str) -> None:
    """tarによる圧縮を行います。

    Args:
        directory_path (str): 保存するディレクトリ
        archive_name (str): アーカイブファイルの名前
    """
    with tarfile.open(archive_name, "w") as tar:
        tar.add(directory_path, arcname="directory")


def extract_tar_archive(extract_path: str, archive_name: str) -> None:
    """tarによる解凍を行います。

    Args:
        extract_path (str): 解凍するパス
        archive_name (str): アーカイブファイルの名前
    """
    with tarfile.open(archive_name, "r") as tar:
        tar.extractall(extract_path)


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
        if force:
            print(f"File {after_path} already exists, will be overwritten.")
        else:
            print(f"File already exists: {after_path}")
            return False
    try:
        os.rename(before_path, after_path)
        return True
    except Exception as e:
        print(f"Error renaming file: {e}")
        return False
