from lib763.macro.core.image_recognition import *
from lib763.macro.core.MouseKeyboard import MouseKeyboard
from lib763.fs.fs import rmrf

from PIL import ImageGrab
import pyperclip
import time


class Macro:
    def __init__(self) -> None:
        self.mk = MouseKeyboard()

    def recog_and_click_img(self, img_path: str):
        self.mk.get_screen_shot("./scshot.png")
        coordinate = get_image_coordinate("./scshot.png", img_path)
        if coordinate is None:
            print("error : no object found")
            return
        self.mk.click_coordinate(coordinate)
        rmrf("./scshot.png")

    def get_mouse_keyboard(self):
        return self.mk

    def get_screen_shot(self, path: str) -> None:
        """
        スクリーンショットを撮影して保存する
        @param:
            path: (str) 保存先のファイルパス
        """
        ImageGrab.grab().save(path)
        time.sleep(self.wait_time)

    def get_clipboard_str(self) -> None:
        """
        クリップボードから文字列を取得する
        @return:
            (str): クリップボードの文字列
        """
        return pyperclip.paste()

    def copy_to_clipboard(self, word: str) -> None:
        """
        文字列をクリップボードにコピーする
        @param:
            word: (str) コピーする文字列
        """
        return pyperclip.copy(word)

    def write_word(self, word: str) -> None:
        """
        クリップボードに文字列をコピーして貼り付ける
        @param:
            word: (str) 貼り付ける文字列
        """
        self.copy_to_clipboard(word)
        self.mk.kb_input("ctrl+v")
        time.sleep(self.wait_time)
