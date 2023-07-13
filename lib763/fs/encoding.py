import chardet
from lib763.fs.save_load import load_str_from_file, save_str_to_file
from lib763.fs.fs import rmrf


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
