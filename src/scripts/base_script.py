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

    def start_relisting(self, image_path: str, sleep_time=17):
        """
        画像あり再出品を実施する
        """
        try:
            mercari_copy_image: tuple = self.screen.image_locate(image_path=image_path)
            pgui.click(mercari_copy_image, duration=0.5)
            self.logger.info("画像あり再出品を選択しました。")
            time.sleep(sleep_time)
            return True
        except Exception as e:
            self.logger.error(e)
            self.logger.error("画像あり再出品を選択できませんでした。処理を終了します。")
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
                self.logger.error(f"出品するボタンが見つかりません。リトライ {attempt + 1}/{retry_limit}")
                if attempt == retry_limit - 1:
                    self.logger.error("リトライの上限に達しました。処理を終了します。")
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
            self.logger.error("出品が完了していません。処理を終了します。")
            return False
        return True