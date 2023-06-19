from lib763.macro.mouse_keyboard import mouse_keyboard
import time
import pyautogui


class chrome_window:
    def __init__(self) -> None:
        self.__mk = mouse_keyboard()
        self.__window_state = False
        self.__tub_count = 0

    def set_window_state(self, flag: bool) -> None:
        self.__window_state = flag

    def get_window_state(self) -> bool:
        return self.__window_state

    def __check_and_ready_window(self):
        """
        chromeが使用可能な状態にする
        """
        if self.__tub_count == 0:
            self.__create_chrome_window()
        if not self.get_window_state():
            self.activate_chrome()

    def activate_chrome(self):
        """
        chromeをアクティブにし、最大化する
        """
        chrome_title = "Google Chrome"
        pyautogui.getWindowsWithTitle(chrome_title)[0].activate()
        pyautogui.getWindowsWithTitle(chrome_title)[0].maximize()
        self.set_window_state(True)

    def create_chrome_window(self) -> None:
        """
        Chromeを立ち上げる
        """
        if self.get_window_state():
            return
        if self.__tub_count > 0:
            self.activate_chrome()
            return
        self.__mk.kb_input("win + r")
        self.__mk.write_word("chrome")
        self.__mk.kb_input("enter")
        self.set_window_state(True)
        self.__tub_count = 1
        time.sleep(2.0)

    def input_url_to_tab(self, url: str) -> None:
        """
        urlを入力する。
        タブが作成された直後に使用される前提。
        """
        self.__check_and_ready_window()
        self.__mk.write_word(url)
        self.__mk.kb_input("enter")
        time.sleep(0.5)

    def create_tab(self):
        """
        新たなタブを作成する。
        """
        self.__mk.kb_input("ctrl+t")
        self.__tub_count += 1

    def erase_tub(self):
        """
        tubを消す
        """
        self.__mk.kb_input("ctrl+w")
        self.__tub_count -= 1
        if self.__tub_count == 0:
            self.set_window_state(False)

    def erase_window(self):
        """
        windowを消す
        """
        self.__mk.keyboard_input("alt+f4")
        self.set_window_state(False)
        self.__tub_count = 0
