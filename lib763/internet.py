import requests
from tqdm import tqdm


def download_file_with_progress(
    url: str, save_path: str, timeout: float = None
) -> bool:
    """
    Downloads a file from the given URL and saves it to the specified path with a progress bar.

    Args:
        url (str): The URL of the file to download.
        save_path (str): The path to save the downloaded file.
        timeout (float, optional): The timeout for the request in seconds. Defaults to None.

    Returns:
        bool: True if the file was downloaded successfully, False otherwise.
    """
    try:
        response = requests.get(url, stream=True, timeout=timeout)
        response.raise_for_status()

        file_size = int(response.headers.get("content-length", 0))
        chunk_size = 1024
        num_bars = int(file_size / chunk_size)

        with open(save_path, "wb") as f, tqdm(
            desc=save_path,
            total=num_bars,
            unit="KB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                bar.update(1)
        print(f"ファイルを保存しました: {save_path}")
        return True
    except requests.RequestException as e:
        print(f"ファイルのダウンロードに失敗しました: {e}")
        return False


def fetch_webpage_text(url: str, timeout: float = None) -> str:
    """
    Fetches the text content of a webpage at the given URL.

    Args:
        url (str): The URL of the webpage to fetch.
        timeout (float, optional): The number of seconds to wait for a response before timing out.

    Returns:
        str: The text content of the webpage, or None if the request failed.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"ウェブページの取得に失敗しました: {e}")
        return None
