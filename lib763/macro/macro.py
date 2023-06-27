from lib763.macro.core.image_recognition import get_image_coordinate
from lib763.macro.core.MouseKeyboard import MouseKeyboard
from lib763.fs.fs import rmrf

from PIL import ImageGrab
import pyperclip
import time


class Macro:
    """マクロ処理を提供するクラス。"""

    def __init__(self) -> None:
        self.mk = MouseKeyboard()

    def recognize_and_click_image(self, image_path: str):
        """画像を認識し、その画像が存在する座標をクリックします。

        Args:
            image_path: 認識させる画像のパス
        """
        screenshot_path = "./screenshot.png"
        self.mk.get_screen_shot(screenshot_path)
        coordinate = get_image_coordinate(screenshot_path, image_path)
        if coordinate is None:
            print("Error: No object found")
            return
        self.mk.click_coordinate(coordinate)
        rmrf(screenshot_path)

    def get_mouse_keyboard(self):
        """MouseKeyboardインスタンスを取得します。

        Returns:
            MouseKeyboardのインスタンス
        """
        return self.mk

    def get_screen_shot(self, path: str) -> None:
        """スクリーンショットを撮影し、指定したパスに保存します。

        Args:
            path: スクリーンショットの保存先パス
        """
        ImageGrab.grab().save(path)
        time.sleep(1)

    def get_clipboard_text(self) -> str:
        """クリップボードからテキストを取得します。

        Returns:
            クリップボードのテキスト
        """
        return pyperclip.paste()

    def copy_to_clipboard(self, text: str) -> None:
        """テキストをクリップボードにコピーします。

        Args:
            text: コピーするテキスト
        """
        pyperclip.copy(text)

    def paste_text(self, text: str) -> None:
        """クリップボードにテキストをコピーし、それを貼り付けます。

        Args:
            text: 貼り付けるテキスト
        """
        self.copy_to_clipboard(text)
        self.mk.kb_input("ctrl+v")
        time.sleep(1)  
