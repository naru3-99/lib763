from lib763.fs import rmrf

import keyboard as kb
import mouse
import time
import pyperclip
import ctypes
import cv2
from PIL import ImageGrab
from typing import Union


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

    def click_image(
        self, image_path: str, screenshot_path: str = "./screenshot.png"
    ) -> None:
        """
        Clicks on an image by taking a screenshot, identifying the image within the screenshot, and clicking on it.

        Args:
            image_path (str): The path of the image to click on.
            screenshot_path (str): The path to save the screenshot to. Defaults to "./screenshot.png".
        """
        self.get_screen_shot(screenshot_path)
        coordinate = get_image_coordinate(screenshot_path, image_path)
        if coordinate is None:
            raise ImageNotFoundError("Error: No object found")
        self.click_coordinate(coordinate)
        rmrf(screenshot_path)

    def get_screen_shot(self, path: str) -> None:
        """
        Takes a screenshot and saves it to a specified path.

        Args:
            path (str): The path to save the screenshot to.
        """
        ImageGrab.grab().save(path)

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

    def get_copied_text(self) -> str:
        """
        Retrieves the text currently copied to the clipboard.

        Returns:
            str: The text currently copied to the clipboard.
        """
        return pyperclip.paste()


def read_image(path: str):
    """指定されたパスから画像を読み込む"""
    img = cv2.imread(path)
    if img is None:
        raise ImageReadError(f"Error reading image from path: {path}")
    return img


def image_contains(all_picture_path: str, target_picture_path: str) -> bool:
    """
    Args:
        all_picture_path (str): 全体画像のパス
        target_picture_path (str): 対象画像のパス

    Returns:
        bool: 全体画像が対象画像を完全に含んでいるかどうか
    """
    template = read_image(all_picture_path)
    image = read_image(target_picture_path)
    result = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
    _, maxVal, _, _ = cv2.minMaxLoc(result)
    return maxVal > 0.99


def get_image_coordinate(
    all_picture_path: str, target_picture_path: str
) -> Union[tuple, None]:
    """
    Args:
        all_picture_path (str): 全体画像のパス
        target_picture_path (str): 対象画像のパス

    Returns:
        tuple | None: 対象画像が全体画像の中に含まれている座標（中心点）
    """
    template = read_image(all_picture_path)
    image = read_image(target_picture_path)
    result = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
    _, maxVal, _, maxLoc = cv2.minMaxLoc(result)
    if maxVal > 0.99:
        center_x = maxLoc[0] + image.shape[1] // 2
        center_y = maxLoc[1] + image.shape[0] // 2
        return (center_x, center_y)
    return None


def get_subregion_center(
    all_path: str, subreg_path: str, target_path: str
) -> Union[tuple, None]:
    """
    Args:
        all_path (str): フルスクリーン画像のパス
        subreg_path (str): フルスクリーン画像内の目標領域画像のパス
        target_path (str): 領域内の目標画像のパス

    Returns:
        tuple | None: フルスクリーン画像内での目標画像の座標
    """
    template = read_image(all_path)
    image = read_image(subreg_path)
    result = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
    _, maxVal, _, maxLoc = cv2.minMaxLoc(result)
    if maxVal <= 0.98:
        return None

    template[:, :, :] = 0
    template[
        maxLoc[1] : maxLoc[1] + image.shape[0],
        maxLoc[0] : maxLoc[0] + image.shape[1],
        :,
    ] = image

    target = read_image(target_path)
    result = cv2.matchTemplate(target, template, cv2.TM_CCORR_NORMED)
    _, maxVal, _, maxLoc = cv2.minMaxLoc(result)
    if maxVal <= 0.98:
        return None
    center_x = maxLoc[0] + target.shape[1] // 2
    center_y = maxLoc[1] + target.shape[0] // 2
    return (center_x, center_y)


def mask_img(img_path: str, mask_range: tuple) -> None:
    """
    Args:
        img_path (str): マスクを適用したい画像のパス
        mask_range (tuple): マスクを適用する座標範囲 (x1, x2, y1, y2)、
                            ただし x1 < x2、y1 < y2 を満たす必要があります

    この関数は指定した範囲内で画像にマスクを適用します
    """
    x1, x2, y1, y2 = mask_range
    if x1 > x2 or y1 > y2:
        raise ValueError("エラー： x1 > x2 または y1 > y2")

    im = read_image(img_path)
    x, y, _ = im.shape
    if y < x2 or x < y2:
        raise ValueError("エラー： x < x2 または y < y2")

    im[y1:y2, x1:x2] = 0
    cv2.imwrite(img_path, im)


class ImageReadError(Exception):
    """Exception raised for errors in the image reading process."""

    pass


class ImageNotFoundError(Exception):
    """Exception raised when an image is not found within another image."""

    pass


class InvalidCoordinateError(Exception):
    """Exception raised for invalid coordinate inputs."""

    pass
