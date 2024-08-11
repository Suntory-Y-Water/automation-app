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

    def image_locate(self, image_path: str, confidence=0.7):
        """
        Webページ内に該当する画像を認識し、その座標を返す

        画像が存在しない場合は`ImageNotFoundException`が発生するので、キャッチしてNoneを返す
        """
        try:
            return pgui.locateOnScreen(image_path, grayscale=True, confidence=confidence)
        except pgui.ImageNotFoundException:
            return None