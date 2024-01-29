import pyautogui as pgui
import pyperclip as pyper
import time


class WebManager:
    """ブラウザ操作を管理するクラス"""

    @staticmethod
    def get_url():
        """ログ記載用のURLを取得する"""
        pgui.hotkey("ctrl", "l")
        pgui.hotkey("ctrl", "c")
        return pyper.paste()

    def page_click(self, image_locate: str):
        """Webページ内に該当する画像を認識し、その座標をクリックする"""
        try:
            x, y = pgui.center(image_locate)
            pgui.click(x, y, duration=0.5)
            return True
        except TypeError:
            return False

    def page_back(self, count: int):
        """Webページを回数分戻る"""
        try:
            for _ in range(count):
                pgui.hotkey("alt", "left")
            return True
        except Exception as e:
            return False

    def go_product_page(self, current_url: str):
        """現在のページが取引画面の場合、商品ページに遷移する"""
        try:
            if "transaction" in current_url:
                new_url = current_url.replace("transaction", "item")
                pyper.copy(new_url)
                pgui.hotkey("ctrl", "l")
                pgui.hotkey("ctrl", "v")
                pgui.press("enter")
                time.sleep(6)
            return True
        except Exception as e:
            # エラー処理
            return False

    @staticmethod
    def printing_process():
        """
        印刷処理を行う。
        印刷時、前の宛名を削除してペーストする。
        """
        try:
            pgui.hotkey("ctrl", "a")
            pgui.press("backspace")
            time.sleep(1)
            pgui.hotkey("ctrl", "v")
            pgui.press("backspace")
            pgui.press("up", presses=9)
            pgui.press("delete", presses=5)
            return True
        except Exception as e:
            # エラー処理
            return False
