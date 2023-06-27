from lib763.macro.core.mouse_keyboard import mouse_keyboard
import time
import pyautogui


class chrome_window:
    """
    このクラスはChromeウィンドウを制御するための機能を提供します。
    """

    def __init__(self) -> None:
        self.__mk = mouse_keyboard()
        self.__window_state = False
        self.__tub_count = 0

    def set_window_state(self, flag: bool) -> None:
        """
        @param:
            flag: (bool) ウィンドウの状態 (True: アクティブ, False: 非アクティブ)
        @return:
            None
        ウィンドウの状態を設定します。
        """
        self.__window_state = flag

    def get_window_state(self) -> bool:
        """
        @param:
            なし
        @return:
            (bool) ウィンドウの状態 (True: アクティブ, False: 非アクティブ)
        ウィンドウの状態を取得します。
        """
        return self.__window_state

    def __check_and_ready_window(self):
        """
        @param:
            なし
        @return:
            None
        ウィンドウの状態を確認し、必要な準備を行います。
        """
        if self.__tub_count == 0:
            self.__create_chrome_window()
        if not self.get_window_state():
            self.activate_chrome()

    def activate_chrome(self):
        """
        @param:
            なし
        @return:
            None
        Chromeウィンドウをアクティブ化し、最大化します。
        """
        chrome_title = "Google Chrome"
        pyautogui.getWindowsWithTitle(chrome_title)[0].activate()
        pyautogui.getWindowsWithTitle(chrome_title)[0].maximize()
        self.set_window_state(True)

    def create_chrome_window(self) -> None:
        """
        @param:
            なし
        @return:
            None
        Chromeウィンドウを作成します。
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
        @param:
            url: (str) 入力するURL
        @return:
            None
        URLを指定したタブに入力します。
        """
        self.__check_and_ready_window()
        self.__mk.write_word(url)
        self.__mk.kb_input("enter")
        time.sleep(0.5)

    def create_tab(self):
        """
        @param:
            なし
        @return:
            None
        新しいタブを作成します。
        """
        self.__mk.kb_input("ctrl+t")
        self.__tub_count += 1

    def erase_tub(self):
        """
        @param:
            なし
        @return:
            None
        現在のタブを閉じます。
        """
        self.__mk.kb_input("ctrl+w")
        self.__tub_count -= 1
        if self.__tub_count == 0:
            self.set_window_state(False)

    def erase_window(self):
        """
        @param:
            なし
        @return:
            None
        ウィンドウを閉じます。
        """
        self.__mk.keyboard_input("alt+f4")
        self.set_window_state(False)
        self.__tub_count = 0
