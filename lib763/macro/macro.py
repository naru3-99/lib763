from lib763.macro.core.image_recognition import get_image_coordinate
from lib763.macro.core.MouseKeyboard import MouseKeyboard
from lib763.fs.fs import rmrf

from PIL import ImageGrab
import pyperclip
import time


class Macro(MouseKeyboard):
    """
    Class for automating mouse and keyboard actions on the computer.

    Inherits from the MouseKeyboard class.

    Attributes:
        wait_time (float): The wait time between keyboard or mouse actions.
    """

    def __init__(self, wait_time=0.5) -> None:
        """
        Constructs all the necessary attributes for the Macro object.

        Args:
            wait_time (float): The wait time between keyboard or mouse actions. Defaults to 0.5.
        """
        super().__init__(wait_time)

    def click_image(self, image_path: str) -> None:
        """
        Clicks on an image by taking a screenshot, identifying the image within the screenshot, and clicking on it.

        Args:
            image_path (str): The path of the image to click on.
        """
        screenshot_path = "./screenshot.png"
        self.get_screen_shot(screenshot_path)
        coordinate = get_image_coordinate(screenshot_path, image_path)
        if coordinate is None:
            print("Error: No object found")
            return
        self.click_coordinate(coordinate)
        rmrf(screenshot_path)

    def get_screen_shot(self, path: str) -> None:
        """
        Takes a screenshot and saves it to a specified path.

        Args:
            path (str): The path to save the screenshot to.
        """
        ImageGrab.grab().save(path)
        time.sleep(1)

    def get_copied_text(self) -> str:
        """
        Retrieves the text currently copied to the clipboard.

        Returns:
            str: The text currently copied to the clipboard.
        """
        return pyperclip.paste()

    def copy_text(self, text: str) -> None:
        """
        Copies a specified text to the clipboard.

        Args:
            text (str): The text to copy to the clipboard.
        """
        pyperclip.copy(text)

    def paste_text(self, text: str) -> None:
        """
        Pastes a specified text by copying it to the clipboard and then simulating a "ctrl+v" keyboard input.

        Args:
            text (str): The text to paste.
        """
        self.copy_text(text)
        self.kb_input("ctrl+v")
        time.sleep(1)
