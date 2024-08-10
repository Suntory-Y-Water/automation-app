import time
import pyautogui as pgui


class ScreenManagement():
    def __init__(self):
        self.screen_width, self.screen_height = pgui.size()

    @staticmethod
    def reloading_page(image_path, wait_time=10.0):
        """指定した画像が読み込めない時にページをリロードする"""
        if image_path is None:
            pgui.press("F5")
            time.sleep(wait_time)

    def image_locate(self, image_path: str) -> tuple:
        """
        Webページ内に該当する画像を認識し、その座標を返す
        そもそも間違った画像だったら例外を吐く
        """
        locate = pgui.locateOnScreen(image_path, grayscale=True, confidence=0.7)
        if not locate:
            raise pgui.ImageNotFoundException

        return locate

    def check_page(self, image_path: str):
        """指定した画像が画面上に存在するか確認する"""
        try:
            is_image = pgui.locateOnScreen(image_path, grayscale=True, confidence=0.7) is not None
            return is_image
        except pgui.ImageNotFoundException:
            return False
