import ctypes
import time
import cv2
import mouse
import keyboard
import pyautogui
import pygetwindow as gw
import numpy as np
from typing import Union, List, Tuple, Optional
from lib763.fs import save_str_to_file, rmrf


## CONST
# constant for display size
DISPLAY_SIZE = pyautogui.size()

# constant for display scale
# this is like 1.5, which means "150%" in windows settings
DISPLAY_SCALE = None
try:
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    DISPLAY_SCALE = user32.GetDpiForSystem() / 96.0
except Exception:
    print("Be careful. DISPLAY_SCALE is not set.")
    pass


class ImageReadError(Exception):
    """Exception raised for errors in the image reading process."""

    pass


class ImageNotFoundError(Exception):
    """Exception raised when an image is not found within another image."""

    pass


class InvalidCoordinateError(Exception):
    """An exception raised when an invalid coordinate is given."""

    pass


def screen_shot(save_path: str = None):
    """画面全体のスクリーンショットを取得する。

    Args:
        save_path (Optional[str]): 保存先のファイルパス。指定しない場合は保存しない。

    Returns:
        Union[None, Image]: 画像オブジェクト。save_pathが指定された場合はNone。
    """
    return pyautogui.screenshot(save_path)


def alert_box(text):
    """アラートボックスを表示する。

    Args:
        text (str): アラートボックスに表示するテキスト。
    """
    pyautogui.alert(text)


def type_write(words: str) -> None:
    """文字列をタイプする。

    Args:
        words (str): 入力する文字列。
    """
    pyautogui.typewrite(words)


def hotkey(*button: str, interval: float = 0.1) -> None:
    """ホットキーを押す。

    Args:
        *button (str): 押すボタン。可変長引数。
        interval (float): 各キー押下の間隔（秒）。
    """
    pyautogui.hotkey(*button, interval=interval)


def scroll(amount: int) -> None:
    """マウススクロールをする。

    Args:
        amount (int): スクロール量。
    """
    pyautogui.scroll(amount)


def keep_clicking(button: str = "left") -> None:
    """マウスボタンを押し続ける。

    Args:
        button (str): 押し続けるボタン（"left", "right" など）。
    """
    mouse.press(button)


def release_clicking(button: str = "left") -> None:
    """マウスボタンを離す。

    Args:
        button (str): 離すボタン（"left", "right" など）。
    """
    mouse.release(button)


def move_mouse(coordinate: Tuple[int, int]) -> bool:
    """マウスポインタを移動する。

    Args:
        coordinate (Tuple[int, int]): 移動先の座標 (x, y)。

    Returns:
        bool: 座標が有効な場合はTrue、それ以外はFalse。
    """
    try:
        x, y = coordinate
    except ValueError:
        return False
    pyautogui.moveTo(x=x, y=y)
    return True


def __validate_coordinate(coordinate: Tuple[int, int]) -> Tuple[int, int]:
    """座標が有効かどうかを検証する。

    Args:
        coordinate (Tuple[int, int]): 検証する座標 (x, y)。

    Returns:
        Tuple[int, int]: 有効な座標。

    Raises:
        InvalidCoordinateError: 座標が無効な場合。
    """
    try:
        x, y = coordinate
        if not (type(x) == int and type(y) == int):
            raise TypeError(f"coordinate must be (int,int), got ({type(x)},{type(y)})")
        if not (pyautogui.onScreen(x, y)):
            raise ValueError(f"given coordinate is not on screen")
    except:
        raise InvalidCoordinateError("coordinate is invalid")
    return x, y


def image_range_to_coordinate(img_range: Tuple[int, int, int, int]) -> Tuple[int, int]:
    """画像範囲から中心座標を計算する。

    Args:
        img_range (Tuple[int, int, int, int]): 画像の左上と右下の座標 (x1, y1, x2, y2)。

    Returns:
        Tuple[int, int]: 画像の中心座標 (x, y)。
    """
    return (
        int((img_range[0] + img_range[2]) / 2),
        int((img_range[1] + img_range[3]) / 2),
    )


def click_coordinate(coordinate: Tuple[int, int], count: int = 1) -> None:
    """指定した座標をクリックする。

    Args:
        coordinate (Tuple[int, int]): クリックする座標 (x, y)。
        count (int, optional): クリック回数。 Defaults to 1。

    Raises:
        InvalidCoordinateError: 座標が無効な場合。
    """
    x, y = __validate_coordinate(coordinate)
    pyautogui.click(x=x, y=y, clicks=count)


def click_image(img_path: str, count: int = 1) -> bool:
    """画像に対応する座標をクリックする。

    Args:
        img_path (str): クリック対象の画像のパス。
        count (int, optional): クリック回数。 Defaults to 1。

    Returns:
        bool: クリックが成功した場合はTrue。
    """
    coordinate = get_image_coordinate_on_screen(img_path)
    if coordinate is None:
        return False
    click_coordinate(coordinate, count=count)
    return True


def drag(
    coordinate_ls: List[Tuple[int, int]],
    duration: float = 1.0,
    left_click: bool = False,
    start_coordinate: Optional[Tuple[int, int]] = None,
) -> None:
    """ドラッグ操作を実行する。

    Args:
        coordinate_ls (List[Tuple[int, int]]): ドラッグする座標のリスト。
        duration (float, optional): ドラッグ操作の時間。 Defaults to 1.0。
        left_click (bool, optional): 左クリックを使用する場合はTrue。 Defaults to False。
        start_coordinate (Optional[Tuple[int, int]], optional): ドラッグの開始座標。 Defaults to None。

    Raises:
        InvalidCoordinateError: 座標が無効な場合。
    """
    # validate coordinate
    coordinate_ls_mod = []
    if start_coordinate == None:
        # Perform a drag operation on the coordinates given in coordinate_ls.
        start_x, start_y = __validate_coordinate(coordinate_ls[0])
        coordinate_ls_mod = [__validate_coordinate(c) for c in coordinate_ls[1:]]
    else:
        # Perform a drag operation on the coordinates given in coordinate_ls,
        # relative to the start point given in start_coordinate.
        start_x, start_y = __validate_coordinate(start_coordinate)
        before_x, before_y = __validate_coordinate(coordinate_ls[0])
        for c in coordinate_ls[1:]:
            x, y = __validate_coordinate(c)
            coordinate_ls_mod.append((x - before_x, y - before_y))
            before_x, before_y = x, y

    # move mouse to start coordinate
    move_mouse(x=start_x, y=start_y)
    # press and hold the left-click button.
    if left_click:
        keep_clicking(button="left")

    # start to drag
    for x, y in coordinate_ls_mod:
        if start_coordinate == None:
            move_mouse(x=x, y=y, duration=duration)
        else:
            pyautogui.moveRel(x=x, y=y, duration=duration)
    # release the right-click button
    if left_click:
        release_clicking(button="left")


def __read_image(path: str):
    """指定されたパスから画像を読み込む"""
    img = cv2.imread(path)
    if img is None:
        raise ImageReadError(f"Error reading image from path: {path}")
    return img


def image_contains(all_picture_path: str, target_picture_path: str) -> bool:
    """画像が別の画像に含まれているか確認する。

    Args:
        all_picture_path (str): 全体画像のパス。
        target_picture_path (str): ターゲット画像のパス。

    Returns:
        bool: ターゲット画像が全体画像に含まれている場合はTrue。
    """
    template = __read_image(all_picture_path)
    image = __read_image(target_picture_path)
    result = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
    _, maxVal, _, _ = cv2.minMaxLoc(result)
    return maxVal > 0.99


def is_image_on_screen(target_picture_path: str) -> bool:
    """ターゲット画像がスクリーンに表示されているか確認する。

    Args:
        target_picture_path (str): ターゲット画像のパス。

    Returns:
        bool: ターゲット画像がスクリーンに表示されている場合はTrue。
    """
    screen_shot_path = "./screenshot.png"
    screen_shot(screen_shot_path)
    ret = image_contains(screen_shot_path, target_picture_path)
    rmrf(screen_shot_path)
    return ret


def get_image_coordinate(
    all_picture_path: str, target_picture_path: str
) -> Union[Tuple[int, int], None]:
    """ターゲット画像の座標を取得する。

    Args:
        all_picture_path (str): 全体画像のパス。
        target_picture_path (str): ターゲット画像のパス。

    Returns:
        Union[Tuple[int, int], None]: ターゲット画像の座標（ターゲット画像が全体画像に含まれない場合はNone）。
    """
    image_range = get_image_range(all_picture_path, target_picture_path)
    if image_range is None:
        return None
    return image_range_to_coordinate(image_range)


def get_image_range(
    all_picture_path: str, target_picture_path: str
) -> Union[Tuple[int, int, int, int], None]:
    """ターゲット画像の範囲（座標）を取得する。

    Args:
        all_picture_path (str): 全体画像のパス。
        target_picture_path (str): ターゲット画像のパス。

    Returns:
        Union[Tuple[int, int, int, int], None]: ターゲット画像の範囲（ターゲット画像が全体画像に含まれない場合はNone）。
    """
    template = __read_image(all_picture_path)
    image = __read_image(target_picture_path)
    result = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
    _, maxVal, _, maxLoc = cv2.minMaxLoc(result)
    if maxVal > 0.99:
        return (
            maxLoc[0],
            maxLoc[1],
            maxLoc[0] + image.shape[1],
            maxLoc[1] + image.shape[0],
        )
    return None


def get_image_coordinate_on_screen(
    target_picture_path: str,
) -> Union[Tuple[int, int], None]:
    """スクリーン上のターゲット画像の座標を取得する。

    Args:
        target_picture_path (str): ターゲット画像のパス。

    Returns:
        Union[Tuple[int, int], None]: ターゲット画像の座標（スクリーンに表示されていない場合はNone）。
    """
    screen_shot_path = "./screenshot.png"
    screen_shot(screen_shot_path)
    ret = get_image_coordinate(screen_shot_path, target_picture_path)
    rmrf(screen_shot_path)
    return ret


def get_all_coordinate_on_screen(target_picture_path: str) -> List[Tuple[int, int]]:
    """スクリーン上でターゲット画像が現れるすべての座標を取得する。

    Args:
        target_picture_path (str): ターゲット画像のパス。

    Returns:
        List[Tuple[int, int]]: ターゲット画像の座標のリスト。
    """
    ret_ls = []
    screen_shot_path = "./screenshot.png"
    screen_shot(screen_shot_path)
    while True:
        img_range = get_image_range(screen_shot_path, target_picture_path)
        if img_range is None:
            rmrf(screen_shot_path)
            return ret_ls
        ret_ls.append(image_range_to_coordinate(img_range))
        __mask_img(screen_shot_path, img_range)


def __mask_img(target_picture_path: str, mask_range: Tuple[int, int, int, int]) -> bool:
    """画像から特定の範囲をマスクする（黒く塗りつぶす）。

    Args:
        target_picture_path (str): 対象の画像のパス。
        mask_range (Tuple[int, int, int, int]): マスクする範囲。

    Returns:
        bool: マスクが成功した場合はTrue。
    """
    try:
        x1, y1, x2, y2 = mask_range
    except:
        return False
    img = __read_image(target_picture_path)
    img[x1:x2, y1:y2] = 0
    cv2.imwrite(target_picture_path, img)
    return True


def get_all_window_names():
    return gw.getAllTitles()


def get_window(name):
    target_name = name.lower()
    all_window_name_ls = get_all_window_names()
    target_windows = [win for win in all_window_name_ls if target_name in win.lower()]
    if len(target_windows) == 0:
        return
    return gw.getWindowsWithTitle(target_windows[0])[0]


def maximize_window(name):
    window = get_window(name)
    if window == None:
        return False
    if not window.isMaximized:
        window.maximize()
    return True


def minimize_window(name):
    window = get_window(name)
    if window == None:
        return False
    if not window.isMinimized:
        window.minimize()
    return True


def get_active_window():
    return gw.getActiveWindow()


def activate_window(name):
    window = get_window(name)
    if window == None:
        return False
    if window.isActive:
        window.activate()
    return False


class RecordDrag:
    def __init__(self):
        self.drag_record = []
        self.start_time = 0

    def record_drag_operation(self, save_path: str):
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
        self.drag_record.append(
            (event.x, event.y, round(time.time() - self.start_time, 5))
        )
