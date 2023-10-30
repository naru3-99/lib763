import ctypes
import time
import mouse
import keyboard
import pyautogui

from lib763.fs import save_str_to_file


# This Macro Library is for Windows Only


class Macro:
    # CONSTs
    # DISPLAY_SIZE = (1920,1080)
    # DISPLAY_SCALE = 1.5(150%)
    def __init__(self, wait_time=0.1) -> None:
        """
        Initializes the Macro object with a specified wait time.

        Args:
        - wait_time: A float representing the wait time between actions.
        """
        # set pause time
        pyautogui.PAUSE = wait_time
        # constant for display size
        self.DISPLAY_SIZE = pyautogui.size()

        # constant for display scale
        # this is like 1.5, which means "150%" in windows settings
        self.DISPLAY_SCALE = None
        try:
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            self.DISPLAY_SCALE = user32.GetDpiForSystem() / 96.0
        except Exception:
            print("Be careful. DISPLAY_SCALE is not set.")
            pass

    def __validate_coordinate(self, coordinate):
        """
        Validates if a given coordinate is on screen.

        Args:
        - coordinate: A tuple representing the x and y coordinates.

        Returns:
        - A tuple representing the x and y coordinates.
        """
        try:
            x, y = coordinate
            if not (type(x) == int and type(y) == int):
                raise TypeError(
                    f"coordinate must be (int,int), got ({type(x)},{type(y)})"
                )
            if not (pyautogui.onScreen(x, y)):
                raise ValueError(f"given coordinate is not on screen")
        except:
            raise InvalidCoordinateError("coordinate is invalid")
        return x, y

    # keyboard functions
    def type_write(self, words):
        """
        Types the given string.

        Args:
        - words: A string representing the text to be typed.
        """
        pyautogui.typewrite(words)

    def hotkey(self, *button, interval=0.1):
        """
        Simulates a hotkey press.

        Args:
        - button: A tuple representing the keys to be pressed.
        - interval: A float representing the time between key presses.
        """
        pyautogui.hotkey(button, interval=interval)

    # mouse functions
    def scroll(self, amount):
        """
        Scrolls the mouse wheel.

        Args:
        - amount: An integer representing the amount to scroll.
        """
        pyautogui.scroll(amount)

    def click_coordinate(self, coordinate, count=1):
        """
        Clicks on a given coordinate.

        Args:
        - coordinate: A tuple representing the x and y coordinates.
        - count: An integer representing the number of clicks to perform.
        """
        x, y = self.__validate_coordinate(coordinate)
        pyautogui.click(x=x, y=y, clicks=count)

    def click_image(self, img_path, count=1):
        """
        Assuming there is only one image on the screen, click on that center of image.

        Args:
        - img_path: A string representing the path to the image file.
        - count: An integer representing the number of clicks to perform.
        """
        x, y = pyautogui.locateCenterOnScreen(img_path)
        pyautogui.click(x=x, y=y, clicks=count)

    def drag(
        self,
        coordinate_ls,
        duration: float = 1,
        left_click: bool = False,
        start_coordinate=None,
    ) -> None:
        """
        Perform a drag operation on the coordinates given in coordinate_ls.
        if start_coordinate is set, relative coordinate is used.

        Args:
        - coordinate_ls: A list of tuples representing the x and y coordinates.
        - duration: A float representing the duration of the drag operation.
        - left_click: A boolean representing whether to perform a left-click drag.
        - start_coordinate: A tuple representing the starting x and y coordinates.

        Returns:
        - None
        """
        # validate coordinate
        coordinate_ls_mod = []
        if start_coordinate == None:
            # Perform a drag operation on the coordinates given in coordinate_ls.
            start_x, start_y = self.__validate_coordinate(coordinate_ls[0])
            coordinate_ls_mod = [
                self.__validate_coordinate(c) for c in coordinate_ls[1:]
            ]
        else:
            # Perform a drag operation on the coordinates given in coordinate_ls,
            # relative to the start point given in start_coordinate.
            start_x, start_y = self.__validate_coordinate(start_coordinate)
            before_x, before_y = self.__validate_coordinate(coordinate_ls[0])
            for c in coordinate_ls[1:]:
                x, y = self.__validate_coordinate(c)
                coordinate_ls_mod.append((x - before_x, y - before_y))
                before_x, before_y = x, y

        # move mouse to start coordinate
        pyautogui.moveTo(x=start_x, y=start_y)
        # press and hold the left-click button.
        if left_click:
            mouse.press(button="left")

        # start to drag
        for x, y in coordinate_ls_mod:
            if start_coordinate == None:
                pyautogui.moveTo(x=x, y=y, duration=duration)
            else:
                pyautogui.moveRel(x=x, y=y, duration=duration)
        # release the right-click button
        if left_click:
            mouse.release(button="left")

    # other functions
    def screen_shot(self, save_path=None):
        """
        Takes a screenshot and saves it to a file.

        Args:
        - save_path: A string representing the path to save the screenshot.
        """
        return pyautogui.screenshot(save_path)

    def alert_box(self, text):
        """
        Displays an alert box with the given text.

        Args:
        - text: A string representing the text to be displayed.
        """
        pyautogui.alert(text)

    def get_all_coordinate(self, img_path):
        """
        Returns a list of all coordinates(center of image)
        where a given image is found.

        Args:
        - img_path: A string representing the path to the image file.

        Returns:
        - A list of tuples representing the x and y coordinates.
        """
        ret_ls = []
        for x1, y1, x2, y2 in pyautogui.locateAllOnScreen(img_path):
            ret_ls.append((int((x1 + x2) / 2), int((y1 + y2) / 2)))
        return ret_ls


class RecordDrag:
    def __init__(self):
        self.drag_record = []
        self.start_time = 0

    def record_drag_operation(self, save_path: str):
        """
        Records a drag operation and saves it to a file.

        Args:
        - save_path: A string representing the path to save the recorded drag operation.
        """
        self.drag_record = []
        self.start_time = time.time()
        mouse.hook(self._record_mouse)

        print("Recording started. Press 'f' to stop recording.")
        keyboard.wait("f")
        mouse.unhook(self._record_mouse)

        save_str_to_file(
            "\n".join([f"{x},{y},{t}" for x, y, t in self.drag_record]), save_path
        )
        print(f"Recording stopped. Saved file: {save_path}")

    def _record_mouse(self, event) -> None:
        """
        Records the mouse event.

        Args:
        - event: A mouse event.
        """
        self.drag_record.append(
            (event.x, event.y, round(time.time() - self.start_time, 5))
        )


class InvalidCoordinateError(Exception):
    """
    An exception raised when an invalid coordinate is given.
    """

    pass
