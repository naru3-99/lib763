"""
2023/05/19
auther:naru
encoding=utf-8
"""

import time
import keyboard as kb
import mouse
import pyperclip
from PIL import ImageGrab
import ctypes


class mouse_keyboard:
    def __init__(self, wait_time=0.5) -> None:
        self.wait_time = wait_time
        self.display_scale = self.__get_display_scale()

    def __get_display_scale(self) -> float:
        """
        Returns:
            float: ディスプレイの倍率
        """
        try:
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            return user32.GetDpiForSystem() / 96.0
        except Exception as e:
            print("Error:", e)
            return None

    def __adjust_coordinate(self, coordinate: tuple) -> tuple:
        """
        Args:
            coordinate (tuple): 座標(x,y)
        Returns:
            tuple: 座標(x,y)をディスプレイの拡大・縮小の倍率で割ったもの
        座標をディスプレイの倍率に合わせて補正する
        """
        return coordinate[0] // self.display_scale, coordinate[1] // self.display_scale

    def kb_input(self, input_str: str) -> None:
        """
        @param:
            inputstr=(String)入力する文字列
        @return:
            None
        """
        kb.press_and_release(input_str)
        time.sleep(self.wait_time)

    def write_word(self, word: str) -> None:
        """
        @param:
            word=(str)書き込む文字列
        @return:
            None
        """
        self.copy_to_clipboard(word)
        self.kb_input("ctrl+v")
        time.sleep(self.wait_time)

    def backspace(self, times: int):
        """
        @param:
            times=(int)削除する文字数
        @return:
            None
        """
        for _ in range(times):
            kb.press_and_release("backspace")
        time.sleep(self.wait_time)

    def __move_mouse(self, x: float, y: float) -> None:
        """
        @param:
            x,y=(float)座標
        @return:
            None
        """
        mouse.move(x, y, absolute=True, duration=0)
        time.sleep(self.wait_time)

    def move_mouse(self, coordinate: tuple) -> None:
        """
        @param:
            coordinate =(int,int) マウスポイントする座標
        @return:
            None
        """
        coord = self.__adjust_coordinate(coordinate)
        self.__move_mouse(float(coord[0]), float(coord[1]))

    def click(self) -> None:
        """
        @param:
            None
        @return:
            None
        """
        mouse.click("left")
        time.sleep(self.wait_time)

    def click_coordinate(self, coordinate: tuple) -> None:
        """
        @param:
            coordinate =(int,int) クリックする座標
        @return:
            None
        """
        self.move_mouse(coordinate)
        self.click()

    def scroll(self) -> None:
        """
        @param:
            None
        @return:
            None
        """
        mouse.wheel(-1)
        time.sleep(self.wait_time)

    def get_screen_shot(self, path: str) -> None:
        """
        @param:
            path=str 保存先
        @return:
            None
        """
        ImageGrab.grab().save(path)
        time.sleep(self.wait_time)

    def get_clipboard_str(self) -> None:
        """
        @param:
            None
        @return:
            None
        """
        return pyperclip.paste()

    def copy_to_clipboard(self, word: str) -> None:
        """
        @param:
            word =(str)
        @return:
            None
        """
        return pyperclip.copy(word)
