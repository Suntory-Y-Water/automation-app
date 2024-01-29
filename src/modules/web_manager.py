import pyautogui as pgui
import pyperclip as pyper


class WebManager:
    """ブラウザ操作を管理するクラス"""

    @staticmethod
    def get_log_url():
        """ログ記載用のURLを取得する"""
        pgui.hotkey("ctrl", "l")
        pgui.hotkey("ctrl", "c")
        return pyper.paste()

    def page_click(self, image_locate: str):
        """Webページ内に該当する画像を認識し、その座標をクリックする"""
        x, y = pgui.center(image_locate)
        pgui.click(x, y, duration=0.5)

    def page_back(self, count: int):
        """Webページを回数分戻る"""
        for _ in range(count):
            pgui.hotkey("alt", "left")
