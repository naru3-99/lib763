import time
import keyboard as kb
import mouse
import ctypes


class InvalidCoordinateError(Exception):
    """Exception raised for invalid coordinate inputs."""

    pass


class MouseKeyboard:
    """
    Class for controlling a computer's mouse and keyboard.

    Attributes:
        wait_time (float): The wait time between keyboard or mouse actions.
        display_scale (float): The scale of the display.
    """

    def __init__(self, wait_time=0.5) -> None:
        """
        Constructs all the necessary attributes for the MouseKeyboard object.

        Args:
            wait_time (float): The wait time between keyboard or mouse actions. Defaults to 0.5.
        """
        self.wait_time = wait_time
        self.display_scale = self.__get_display_scale()

    def __get_display_scale(self) -> float:
        """
        Retrieves the display scale by interacting with the operating system.

        Returns:
            float: The scale of the display.
        """
        try:
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            return user32.GetDpiForSystem() / 96.0
        except Exception as e:
            print("Error:", e)
            return 1.0

    def kb_input(self, input_str: str) -> None:
        """
        Simulates a keyboard input.

        Args:
            input_str (str): The string to input via the keyboard.
        """
        kb.press_and_release(input_str)
        time.sleep(self.wait_time)

    def backspace(self, times: int):
        """
        Simulates pressing the backspace key a certain number of times.

        Args:
            times (int): The number of times to press backspace.
        """
        for _ in range(times):
            kb.press_and_release("backspace")
        time.sleep(self.wait_time)

    def click(self) -> None:
        """
        Simulates a left mouse click.
        """
        mouse.click("left")
        time.sleep(self.wait_time)

    def click_coordinate(self, coordinate: tuple) -> None:
        """
        Moves the mouse to a certain coordinate and clicks.

        Args:
            coordinate (tuple): The coordinates to move the mouse to. Should be in the form (x, y).
        """
        try:
            x, y = coordinate
            if x is None or y is None:
                raise InvalidCoordinateError(
                    "One or both of the coordinates are None. Maybe the image couldn't be recognized."
                )
        except ValueError:
            print("coordinate is None")
            return
        self.move_mouse(coordinate)
        self.click()

    def move_mouse(self, coordinate: tuple) -> None:
        """
        Moves the mouse to a certain coordinate.

        Args:
            coordinate (tuple): The coordinates to move the mouse to. Should be in the form (x, y).
        """
        x, y = (
            coordinate[0] // self.display_scale,
            coordinate[1] // self.display_scale,
        )
        mouse.move(x, y, absolute=True, duration=0)
        time.sleep(self.wait_time)

    def scroll(self, times: int) -> None:
        """
        Simulates scrolling the mouse wheel a certain number of times.

        Args:
            times (int): The number of times to scroll the mouse wheel.
        """
        for _ in range(times):
            mouse.wheel(-1)
        time.sleep(self.wait_time)
