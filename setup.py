from setuptools import setup, find_packages

setup(
    name="lib763",
    version="0.3.8",
    description="naru's library",
    author="naru",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "paramiko",
        "chardet",
        "opencv-python",  # cv2 is provided by opencv-python
        "keyboard",
        "mouse",
        "pyperclip",
        "pyautogui",
    ],
)
