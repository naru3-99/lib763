import time
import keyboard as kb
import mouse
import pyperclip
from PIL import ImageGrab
import ctypes


class MouseKeyboard:
    def __init__(self, wait_time=0.5) -> None:
        """
        コンストラクタ
        @param:
            wait_time: (float) 待機時間
        """
        self.wait_time = wait_time
        self.display_scale = self.__get_display_scale()

    def __get_display_scale(self) -> float:
        """
        ディスプレイのスケールを取得する
        @return:
            (float): ディスプレイのスケール値
        """
        try:
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            return user32.GetDpiForSystem() / 96.0
        except Exception as e:
            print("Error:", e)
            return 1.0

    # 省略

    def backspace(self, times: int):
        """
        バックスペースキーを指定回数押す
        @param:
            times: (int) バックスペースキーを押す回数
        """
        for _ in range(times):
            kb.press_and_release("backspace")
        time.sleep(self.wait_time)

    # 省略

    def scroll(self) -> None:
        """
        マウススクロールを行う
        """
        for _ in range(2):
            mouse.wheel(-1)
        time.sleep(self.wait_time)

    def click_coordinate(self, coordinate: tuple) -> None:
        """
        マウスを指定座標に移動してクリックする
        @param:
            coordinate: (tuple) クリック座標 (x, y)
        """
        try:
            x, y = coordinate
            if x is None or y is None:
                raise ValueError
        except ValueError:
            print("coordinate is None\nmaybe couldn't recognize image")
            return
        self.move_mouse(coordinate)
        self.click()
