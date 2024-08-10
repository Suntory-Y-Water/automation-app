from .base_script import BaseScript
from modules.logger import Logger
from modules.screen import ScreenManagement
from modules.web_manager import WebManager
import pyautogui as pgui
import time


class AutoRelistSoldItems(BaseScript):
    """自動再出品(売れた商品)"""

    def __init__(self):
        super().__init__()
        self.logger = Logger.setup_logger("auto_relist_sold_items")
        self.screen = ScreenManagement()
        self.web = WebManager()
        self.logger.info("売れた商品の自動再出品を開始します")

    def run(self, count=1, retry_limit=3):
        self.logger.info("---------------start---------------")
        for _ in range(count):
            current_url = self.web.get_url()
            self.web.go_product_page(current_url)

            self.logger.info(f"この商品を再出品します。商品URL: {self.web.get_url()}")
            try:
                mercari_copy_image: tuple = self.screen.image_locate(image_path="./images/mercari_copy.png")
                pgui.click(mercari_copy_image, duration=0.5)
                self.logger.info("画像あり再出品を選択")
                time.sleep(17)
            except Exception as e:
                self.logger.error(e)
                self.logger.error("画像あり再出品を選択できませんでした。処理を終了します。")
                break

            # 出品するボタンを押すために画面一番下へスクロール
            for attempt in range(retry_limit):
                pgui.press("end")
                time.sleep(2)
                try:
                    relist_image: tuple = self.screen.image_locate(image_path="./images/syuppinnsuru.png")
                    pgui.click(relist_image, duration=0.5)
                    self.logger.info("出品するボタンを押下")
                    time.sleep(2)
                    break  # 成功した場合、ループを抜ける
                except pgui.ImageNotFoundException as e:
                    self.logger.error(f"出品するボタンが見つかりません。リトライ {attempt + 1}/{retry_limit}")
                    if attempt == retry_limit - 1:
                        self.logger.error("リトライの上限に達しました。処理を終了します。")
                        raise e
                    time.sleep(1)  # リトライ間の待機時間

            # 出品が完了しているか確認
            fix_relist_check1 = self.screen.check_page(image_path="./images/syuppindekiteiruka.png")
            fix_relist_check2 = self.screen.check_page(image_path="./images/syuppindekiteiruka.png")
            # 出品が完了しているか確認
            if fix_relist_check1 and fix_relist_check2 == False:
                self.logger.error("出品が完了していません。処理を終了します。")
                break

            pgui.hotkey("ctrl", "w")
            self.logger.info("出品が完了したため、次の商品を再出品します。")
        self.logger.info("売れた商品の自動再出品を終了します")
        self.logger.info("----------------end----------------")
        pgui.alert(text="売れた商品の自動再出品を終了します", title="終了通知", button="OK")
