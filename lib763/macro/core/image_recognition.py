import cv2
from typing import Union


def read_image(path: str):
    """指定されたパスから画像を読み込む"""
    return cv2.imread(path)


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
