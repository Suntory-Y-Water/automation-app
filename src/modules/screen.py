import time
import pyautogui as pgui
from logger import Logger


class ScreenManagement:
    def __init__(self):
        self.screen_width, self.screen_height = pgui.size()
        self.image_base_path = "../images"  # 画像のベースパスを設定

    @staticmethod
    def reloading_page(image_path, wait_time=10.0):
        """指定した画像が読み込めない時にページをリロードする"""
        if image_path is None:
            pgui.press("F5")
            # logger.debug("画像が読み込めないためリロードします。")
            time.sleep(wait_time)

    def image_locate(self, image_path: str) -> tuple:
        """Webページ内に該当する画像を認識し、その座標を返す"""
        locate = pgui.locateOnScreen(image_path, grayscale=True, confidence=0.7)

        try:
            locate = pgui.locateOnScreen(image_path, grayscale=True, confidence=0.7)
            if not locate:
                raise pgui.ImageNotFoundException
        except pgui.ImageNotFoundException:
            # self.logger.error(f"エラー: {image_path} が画面上に見つかりませんでした。")
            return None

        return locate

    def check_page(self, image_path: str):
        """指定した画像が画面上に存在するか確認する"""
        return pgui.locateOnScreen(image_path, grayscale=True, confidence=0.7) is not None
