from lib763.macro.core.MouseKeyboard import MouseKeyboard
import time
import pyautogui


class ChromeWindow:
    """Chromeウィンドウの制御機能を提供するクラス。"""

    def __init__(self) -> None:
        self.__mk = MouseKeyboard()
        self.__window_active = False
        self.__tab_count = 0

    def set_window_active(self, is_active: bool) -> None:
        """ウィンドウの活性状態を設定します。

        Args:
            is_active: ウィンドウの活性状態 (True: アクティブ, False: 非アクティブ)
        """
        self.__window_active = is_active

    def get_window_active(self) -> bool:
        """ウィンドウの活性状態を取得します。

        Returns:
            ウィンドウの活性状態 (True: アクティブ, False: 非アクティブ)
        """
        return self.__window_active

    def __prepare_window(self):
        """ウィンドウの状態を確認し、必要な操作を行います。"""
        if self.__tab_count == 0:
            self.__create_chrome_window()
        if not self.get_window_active():
            self.activate_chrome()

    def activate_chrome(self):
        """Google Chromeウィンドウをアクティブにし、最大化します。"""
        chrome_title = "Google Chrome"
        pyautogui.getWindowsWithTitle(chrome_title)[0].activate()
        pyautogui.getWindowsWithTitle(chrome_title)[0].maximize()
        self.set_window_active(True)

    def create_chrome_window(self) -> None:
        """新規Google Chromeウィンドウを作成します。

        既にウィンドウが活性状態、またはタブが開いている場合は、ウィンドウをアクティブにする。
        """
        if self.get_window_active():
            return
        if self.__tab_count > 0:
            self.activate_chrome()
            return
        self.__mk.kb_input("win + r")
        self.__mk.write_word("chrome")
        self.__mk.kb_input("enter")
        self.set_window_active(True)
        self.__tab_count = 1
        time.sleep(2.0)

    def input_url_to_tab(self, url: str) -> None:
        """指定したURLを現在のタブに入力します。

        Args:
            url: 入力するURL
        """
        self.__prepare_window()
        self.__mk.write_word(url)
        self.__mk.kb_input("enter")
        time.sleep(0.5)

    def create_tab(self):
        """新規タブを作成します。"""
        self.__mk.kb_input("ctrl+t")
        self.__tab_count += 1

    def close_tab(self):
        """現在のタブを閉じます。

        すべてのタブが閉じられた場合、ウィンドウの活性状態をFalseに設定します。
        """
        self.__mk.kb_input("ctrl+w")
        self.__tab_count -= 1
        if self.__tab_count == 0:
            self.set_window_active(False)

    def close_window(self):
        """ウィンドウ全体を閉じます。

        この操作後、ウィンドウの活性状態はFalseになり、タブ数は0にリセットされます。
        """
        self.__mk.kb_input("alt+f4")
        self.set_window_active(False)
        self.__tab_count = 0
