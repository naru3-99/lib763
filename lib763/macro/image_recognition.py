import cv2


def image_contains(all_picture_path: str, target_picture_path: str) -> bool:
    """
    @param:
        all_picture_path: str 全体の画像のパス
        target_picture_path: str 対象の画像のパス
    @return:
        bool 対象が全体に含まれているかどうか
    全体画像の中に対象画像が完全一致で含まれている->true
    """
    template = cv2.imread(all_picture_path)
    image = cv2.imread(target_picture_path)
    result = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    return maxVal > 0.99


def get_image_coordinate(all_picture_path: str, target_picture_path: str) -> tuple | None:
    """
    @param:
        all_picture_path: str 全体の画像のパス
        target_picture_path: str 対象の画像のパス
    @return:
        (x, y) 対象が全体に含まれているかどうか
    全体画像の中に対象画像が完全一致で含まれている座標(中央を返す)
    """
    template = cv2.imread(all_picture_path)
    image = cv2.imread(target_picture_path)
    result = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    if maxVal > 0.99:
        center_x = maxLoc[0] + image.shape[1] // 2
        center_y = maxLoc[1] + image.shape[0] // 2
        return (center_x, center_y)
    return None


def get_subregion_center(all_path: str, subreg_path: str, target_path: str) -> tuple | None:
    """
    Args:
        all_path (str): 全画面の画像ファイルのパス
        subreg_path (str): 全画面のうち、対象となる画像のファイルのパス
        target_path (str): subregのうち、座標が知りたい画像のファイルのパス
    Returns:
        tuple | None: targetの座標
    例えば、スクリーンショットをall_pathとすると、
    (ラジオボタン)_説明となっている画像をsubreg、
    (ラジオボタン)の画像をtargetとすると、
    選択したい対象のラジオボタンの座標をクリックすることができる。
    """
    template = cv2.imread(all_path)
    image = cv2.imread(subreg_path)
    result = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    if maxVal <= 0.98:
        return None

    template[:, :, :] = 0
    template[maxLoc[1] : maxLoc[1] + image.shape[0], maxLoc[0] : maxLoc[0] + image.shape[1], :] = image

    target = cv2.imread(target_path)
    result = cv2.matchTemplate(target, template, cv2.TM_CCORR_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    if maxVal <= 0.98:
        return None
    center_x = maxLoc[0] + target.shape[1] // 2
    center_y = maxLoc[1] + target.shape[0] // 2
    return (center_x, center_y)


def mask_img(img_path: str, mask_range: tuple) -> None:
    """
    @param:
        img_path: str マスクする画像のパス
        mask_range: tuple (x1, x2, y1, y2)
        x1 < x2, y1 < y2とすること。
    @return:
        None
    マスクを行う
    """
    x1, x2, y1, y2 = mask_range
    if x1 > x2 or y1 > y2:
        print("error: x1 > x2 or y1 > y2")
        return

    im = cv2.imread(img_path)
    x, y, z = im.shape
    if y < x2 or x < y2:
        print("error: x < x2 or y < y2")

    im[y1:y2, x1:x2] = 0
    cv2.imwrite(img_path, im)
