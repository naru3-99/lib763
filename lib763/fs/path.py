import glob
import os


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


def get_parent_directory(file_path: str) -> str:
    """ファイルのパスから直下のディレクトリを取得します。

    Args:
        file_path: ファイルのパス

    Returns:
        ファイルの存在する直下のディレクトリのパス
    """
    return os.path.dirname(file_path)


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
