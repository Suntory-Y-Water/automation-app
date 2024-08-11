from .base_script import BaseScript
from modules.logger import Logger
from modules.screen import ScreenManagement
from modules.web_manager import WebManager
import pyautogui as pgui
import time


class AutoRelist(BaseScript):
    """自動再出品(売れていない商品)"""

    def __init__(self):
        super().__init__()
        self.logger = Logger.setup_logger("auto_relist")
        self.screen = ScreenManagement()
        self.web = WebManager()
        self.logger.info("自動再出品を開始します")

    def run(self, count=1):
        self.logger.info("---------------start---------------")
        for _ in range(count):
            self.logger.info(f"この商品を再出品します。商品URL: {self.web.get_url()}")

            try:
                mercari_copy_image: tuple = self.screen.image_locate(image_path="./images/mercari_copy.png")
                pgui.click(mercari_copy_image, duration=0.5)
                self.logger.info("画像あり再出品を選択")
                time.sleep(15)
            except Exception as e:
                self.logger.error(e)
                self.logger.error("画像あり再出品を選択できませんでした。処理を終了します。")
                raise e

            # 出品するボタンを押すために画面一番下へスクロール
            pgui.press("end")
            time.sleep(2)

            try:
                relist_image: tuple = self.screen.image_locate(image_path="./images/syuppinnsuru.png")
                pgui.click(relist_image, duration=0.5)
                self.logger.info("出品するボタンを押下")
                time.sleep(2)
            except Exception as e:
                self.logger.error(e)
                self.logger.error("出品するボタンが選択できませんでした。処理を終了します。")
                raise e

            fix_relist_check1 = self.screen.check_page(image_path="./images/syuppindekiteiruka.png")
            fix_relist_check2 = self.screen.check_page(image_path="./images/syuppindekiteiruka.png")
            # 出品が完了しているか確認
            if fix_relist_check1 and fix_relist_check2 == False:
                self.logger.error("出品が完了していません。処理を終了します。")
                break

            self.web.page_back(count=8)
            self.logger.info("出品が完了したため、商品ページに戻ります。")
            time.sleep(2)

            if self.screen.check_page(image_path="./images/mercari_copy.png") == False:
                self.logger.error("商品ページに戻ることが出来ていません。処理を終了します。")
                break

            # 商品の編集ページで通常のボタンかタイムセールのボタンかを判定
            edit_page = self.screen.check_page(image_path="./images/syouhinnnohensyuu.png")
            edit_time_sale_page = self.screen.check_page(image_path="./images/time-sale-or-syouhinnohensyu.png")
            
            if edit_page:
                edit_item_button: tuple = self.screen.image_locate(image_path="./images/syouhinnnohensyuu.png")
                pgui.click(edit_item_button, duration=0.5)
                self.logger.info("通常の商品編集ボタンを押下しました")
            elif edit_time_sale_page:
                edit_time_sale_button: tuple = self.screen.image_locate(image_path="./images/time-sale-or-syouhinnohensyu.png")
                pgui.click(edit_time_sale_button, duration=0.5)
                self.logger.info("タイムセールの編集ボタンを押下しました")
            else:
                raise Exception("適切な編集ボタンが見つかりませんでした。処理を中止します。")

            # 処理後の待機時間
            time.sleep(3)
            
            pgui.press("end")
            self.logger.info("商品の編集へ移動")
            time.sleep(2)

            try:
                # この商品を削除するボタンを押下
                delete_button: tuple = self.screen.image_locate(image_path="./images/konosyouhinwosakujosuru.png")
                pgui.click(delete_button, duration=0.5)
                time.sleep(1)
            except Exception as e:
                self.logger.error(e)
                self.logger.error("この商品を削除するボタンが選択できませんでした。処理を終了します。")
                raise e

            try:
                # 削除するボタンを押下
                delete_popup_button: tuple = self.screen.image_locate(image_path="./images/sakujosuru.png")
                pgui.click(delete_popup_button, duration=0.5)
                time.sleep(2)
            except Exception as e:
                self.logger.error(e)
                self.logger.error("削除するボタンが選択できませんでした。処理を終了します。")
                raise e

            pgui.hotkey("ctrl", "w")
        self.logger.info("自動再出品を終了します")
        self.logger.info("----------------end----------------")
        pgui.alert(text="自動再出品を終了します", title="終了通知", button="OK")
