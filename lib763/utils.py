import re
from pyperclip import copy, paste


def mold_copied_eng_paper(text):
    """Formats the copied English text by removing unnecessary hyphens and newlines.

    Args:
        text (str): The input text to be formatted.

    Returns:
        str: The formatted text with unnecessary hyphens and newlines removed.
    """
    text1 = re.sub(r"-[\r\n]+", "", text)
    text2 = re.sub(r"[\r\n]+[\r\n]+", " ", text1)
    text3 = re.sub(r"[\r\n]+", " ", text2)
    return text3


def mold_eng_from_clipboard():
    """Formats the text from the clipboard and copies the formatted text back to the clipboard.

    This function retrieves the text from the clipboard, formats it using the
    `mold_copied_eng_paper` function, and then copies the formatted text back to the clipboard.
    """
    text = paste()
    copy(mold_copied_eng_paper(text))
