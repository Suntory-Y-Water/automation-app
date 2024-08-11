from modules.logger import Logger
from modules.screen import ScreenManagement
from modules.web_manager import WebManager
import pyautogui as pgui
import time
import os
import sys

class BaseScript:
    """実行ファイルが格納されているフォルダのベースクラス"""

    def __init__(self):
        self.setup_path()
        self.logger = Logger.setup_logger("auto-relist")
        self.screen = ScreenManagement()
        self.web = WebManager()

    def setup_path(self):
        """スクリプトごとにモジュールパスを設定する"""
        current_dir = os.path.dirname(__file__)
        src_dir = os.path.abspath(os.path.join(current_dir, ".."))
        if src_dir not in sys.path:
            sys.path.append(src_dir)

    def click_and_wait(self, image_path: str, sleep_time=17):
        """
        指定した座標を押下して、押下後に指定した秒数待機する
        初期値は画像あり再出品で使用する17秒を指定
        """
        try:
            click_image: tuple = self.screen.image_locate(image_path=image_path)
            pgui.click(click_image, duration=0.5)
            time.sleep(sleep_time)
            return True
        except Exception as e:
            self.logger.error(e)
            return False

    def scroll_to_bottom_and_click(self, image_path, retry_limit=3):
        """
        出品するボタンを押下する
        押す前に出品するボタンが見つかるまで画面一番下までスクロールする
        """
        # 出品するボタンを押すために画面一番下へスクロール
        for attempt in range(retry_limit):
            pgui.press("end")
            time.sleep(2)
            try:
                relist_image: tuple = self.screen.image_locate(image_path=image_path)
                pgui.click(relist_image, duration=0.5)
                self.logger.info("出品するボタンを押下")
                time.sleep(2)
                return True
            except pgui.ImageNotFoundException:
                self.logger.error(f"出品するボタンが見つかりませんリトライ {attempt + 1}/{retry_limit}")
                if attempt == retry_limit - 1:
                    self.logger.error("リトライの上限に達しました処理を終了します")
                    return False
        return False

    def check_relist(self):
        """
        出品するボタンを押下したあと、出品が完了できているか確認する
        """
        fix_relist_check1 = self.screen.image_locate(image_path="./images/syuppindekiteiruka.png")
        fix_relist_check2 = self.screen.image_locate(image_path="./images/kakakuwokimezunisyuppin.png")

        # 出品が完了しているか確認
        if fix_relist_check1 and fix_relist_check2 == None:
            self.logger.error("出品が完了していません処理を終了します")
            return False
        return True