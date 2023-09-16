import os
import shutil
import zipfile
import fnmatch
import chardet
import glob
import pickle
from typing import Union, List, Optional


def save_object_to_file(obj: object, path: str) -> None:
    """オブジェクトをpickleファイルとして保存します。

    Args:
        obj: 保存するオブジェクト
        path: 保存するパス
    """
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_object_from_file(path: str) -> object:
    """指定したパスのpickleファイルからオブジェクトを読み込みます。

    Args:
        path: 読み込むパス

    Returns:
        保存されていたオブジェクト

    Raises:
        FileNotFoundError: 指定したパスが存在しない場合
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")
    with open(path, "rb") as f:
        obj = pickle.load(f)
    return obj


def save_str_to_file(sentence: str, path: str, encoding="utf-8") -> None:
    """文字列データを指定したパスにテキストファイルとして保存します。

    Args:
        sentence: 文字列データ
        path: 保存するパス
        encoding: エンコーディング
    """
    with open(path, "w", encoding=encoding) as f:
        f.write(sentence)


def append_str_to_file(sentence: str, path: str, encoding="utf-8") -> None:
    """文字列データを指定したパスに追記します。

    Args:
        sentence: 文字列データ
        path: 保存するパス
        encoding: エンコーディング

    Raises:
        FileNotFoundError: 指定したパスが存在しない場合
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")
    with open(path, "a", encoding=encoding) as f:
        f.write(sentence)


def load_str_from_file(path: str, encoding="utf-8") -> str:
    """指定したパスのテキストファイルの内容を取得します。

    Args:
        path: パス

    Returns:
        テキストファイルの内容

    Raises:
        FileNotFoundError: 指定したパスが存在しない場合
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")
    with open(path, "r", encoding=encoding) as f:
        lines = [line.rstrip() for line in f]
    return "\n".join(lines)


def get_file_rows_iter(path: str, encoding="utf-8") -> list:
    """
    Returns an iterator over the rows of a file located at the given path.

    Args:
        path (str): The path to the file.
        encoding (str, optional): The encoding of the file. Defaults to "utf-8".

    Returns:
        list: An iterator over the rows of the file.
    """
    return load_str_from_file(path, encoding=encoding).replace("\n\n", "\n").split("\n")


def get_all_file_path_in(target_dir: str) -> list:
    """指定したディレクトリ内のすべてのファイルのパスを取得します。

    Args:
        target_dir: 対象とするディレクトリ

    Returns:
        対象ディレクトリ内のすべてのファイルのパス
    """
    return [
        path.replace("\\", "/")
        for path in glob.glob(target_dir + "/**/*", recursive=True)
        if (os.path.isfile(path))
    ]


def get_all_dir_path_in(target_dir: str) -> list:
    """指定したディレクトリ内のすべてのサブディレクトリのパスを取得します。

    Args:
        target_dir: 対象とするディレクトリ

    Returns:
        対象ディレクトリ内のすべてのサブディレクトリ
    """
    return [
        path.replace("\\", "/")
        for path in glob.glob(target_dir + "/*/", recursive=True)
        if (os.path.isdir(path))
    ]


def get_all_dir_names_in(target_dir: str) -> list:
    """対象のフォルダ直下のフォルダ名を取得します。

    Args:
        target_dir: 対象のフォルダのパス

    Returns:
        対象のフォルダ直下のフォルダ名
    """
    return [
        dir_name
        for dir_name in os.listdir(target_dir)
        if os.path.isdir(os.path.join(target_dir, dir_name))
    ]


def get_all_file_names_in(target_dir: str) -> list:
    """対象のフォルダ直下のファイル名を取得します。

    Args:
        target_dir: 対象のフォルダのパス

    Returns:
        対象のフォルダ直下のファイル名
    """
    return [
        file_name
        for file_name in os.listdir(target_dir)
        if os.path.isfile(os.path.join(target_dir, file_name))
    ]


def get_file_extension(path: str) -> str:
    """ファイルの拡張子の文字列を取得します。

    Args:
        path: ファイルのパス

    Returns:
        ファイルの拡張子
    """
    return os.path.splitext(path)[-1]


def get_file_name(path: str) -> str:
    """ファイル名の文字列を取得します。

    Args:
        path: ファイルのパス

    Returns:
        ファイルの名前
    """
    return os.path.basename(path)


def get_file_name_without_ext(path: str) -> Optional[str]:
    """ファイルパスからファイル名を取得し、拡張子を除いたものを返す関数

    Args:
        path (str): 対象となるファイルのパス

    Returns:
        Optional[str]: 拡張子を除いたファイル名。パスが無効な場合はNone
    """
    file_name = get_file_name(path)
    return os.path.splitext(file_name)[0] if file_name else None


def get_parent_directory(file_path: str) -> str:
    """ファイルのパスから直下のディレクトリを取得します。

    Args:
        file_path: ファイルのパス

    Returns:
        ファイルの存在する直下のディレクトリのパス
    """
    return os.path.dirname(file_path)


def is_same_path(path1: str, path2: str) -> bool:
    """
    2つのパス文字列が同じパスを表しているかを確認する関数。

    Args:
        path1 (str): 比較する最初のパス。
        path2 (str): 比較する2つ目のパス。

    Returns:
        bool: 2つのパスが同じ場合はTrue、異なる場合はFalse。
    """
    return os.path.normpath(path1) == os.path.normpath(path2)


def get_dir_size(target_dir: str) -> int:
    """指定したディレクトリのサイズを返します。

    Args:
        target_dir: 対象とするディレクトリ

    Returns:
        ディレクトリのサイズ
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
    """指定したファイルのサイズを返します。

    Args:
        target_file: 対象とするファイル

    Returns:
        ファイルのサイズ
    """
    return os.path.getsize(target_file)


def get_file_encoding(path: str) -> str:
    """
    Given a file path, detects and returns the file's encoding.

    Args:
        path (str): The path of the file to read.

    Returns:
        str: The predicted encoding of the file.

    Raises:
        Exception: If there's an error opening/reading the file or detecting its encoding.
    """
    try:
        with open(path, "rb") as f:
            result = chardet.detect(f.read())
        return result["encoding"]
    except Exception as e:
        raise Exception(f"Error occurred while getting file encoding: {e}")


def change_encoding(sentence: str, before: str, after: str) -> str:
    """
    Changes the encoding of a given string.

    Args:
        sentence (str): The string whose encoding needs to be changed.
        before (str): The original encoding of the string.
        after (str): The target encoding to change to.

    Returns:
        str: The string with its encoding changed.

    Raises:
        Exception: If there's an error changing the encoding of the string.
    """
    try:
        return sentence.encode(before).decode(after)
    except Exception as e:
        raise Exception(f"Error occurred while changing encoding: {e}")


def change_file_encoding(path: str, encoding: str) -> None:
    """
    Change the encoding of a file.

    This function reads a file, determines its current encoding,
    reads the contents, deletes the file, and saves the content back to
    a new file with a new encoding.

    Args:
        path: The path to the file.
        encoding: The new encoding to apply to the file.

    Raises:
        IOError: An error occurred accessing the file.
    """
    sentence = load_str_from_file(path, encoding=get_file_encoding(path))
    rmrf(path)
    save_str_to_file(sentence, path, encoding=encoding)


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
        save_str_to_file("", path)
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
    return mkdir(target_dir, str(len(get_all_dir_names_in(target_dir)) + 1))


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
    file_name = f"{len(get_all_file_names_in(target_dir))}.{extension}"
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
    shutil.copy(load_path, save_path)


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
        return True
    except Exception as e:
        print(f"Can't move file: '{src_path}' to '{dst_path}'. Reason: {e}")
        return False


def rename_dir(target_dir: str, after: str) -> None:
    """
    Rename a directory.

    Args:
        target_dir (str): The path to the directory to rename.
        after (str): The new name for the directory.

    Returns:
        None
    """
    os.rename(target_dir, os.path.join(os.path.dirname(target_dir), after))


def create_zip(directory_path, archive_name):
    """zipによる圧縮を行います。

    Args:
        directory_path (str): 保存するディレクトリ
        archive_name (str): アーカイブファイルの名前
    """
    shutil.make_archive(archive_name, "zip", directory_path)


def create_zip_from_list(files: List[str], zip_filename: str) -> List[str]:
    """
    与えられたファイルのパスのリストから、一つのzipファイルを作成する関数。
    存在しないファイルのパスはリストとして返します。

    Args:
        files (List[str]): zipファイルに含めるファイルのパスのリスト。
        zip_filename (str): 作成するzipファイルの名前。

    Returns:
        List[str]: 存在しないファイルのパスのリスト。
    """
    non_existent_files = []
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for file in files:
            if os.path.isfile(file):
                zipf.write(file, os.path.basename(file))
            else:
                non_existent_files.append(file)

    return non_existent_files


def unzip(archive_path, extract_path=None):
    """
    Extract all files from a zip archive.

    Args:
        archive_path (str): The path to the zip file.
        extract_path (str, optional): The path to extract the files to. Defaults to None.

    Returns:
        None
    """
    path = os.path.dirname(archive_path) if extract_path is None else extract_path
    with zipfile.ZipFile(archive_path, "r") as zip_ref:
        zip_ref.extractall(path)


def extract_specific_files(
    zip_path: str, target_files: List[str], extract_path: str = None
) -> None:
    """
    Extract specific files from a zip archive.

    Args:
        zip_path (str): The path to the zip file.
        target_files (List[str]): The list of files to extract.
        extract_path (str): The path to extract the files to.

    Returns:
        None
    """
    path = os.path.dirname(zip_path) if extract_path is None else extract_path
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for target_file in target_files:
            matched_files = fnmatch.filter(zip_ref.namelist(), target_file)
            if matched_files:
                for matched_file in matched_files:
                    zip_ref.extract(matched_file, path)
            else:
                print(f"{target_file} is not found in the zip file.")
