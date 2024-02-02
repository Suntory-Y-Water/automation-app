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
                break

            # # 2024/02/01 現在、カテゴリページでフリーズするため、商品ページに戻る処理を追加
            # # 2024/02/02 現在、改修されたため、カテゴリページでフリーズすることはなくなった
            # if self.screen.check_page(image_path="./images/category_hobby_page.png") == True:
            #     self.web.page_back(count=5)
            #     self.logger.info("カテゴリページでフリーズしたため、商品ページに戻ります。")
            #     time.sleep(2)

            #     # 画像あり再出品ボタンとかぶらなくさせる処置
            #     pgui.moveTo(100, 100)
            #     if self.screen.check_page(image_path="./images/mercari_copy.png") == False:
            #         self.logger.info("商品ページに戻ることが出来ていません。")
            #         self.web.page_back(count=1)
            #         time.sleep(1)

            #     # 商品ページから再出品を実行するため、次へキーで編集ページへ移動
            #     pgui.hotkey("alt", "right")
            #     time.sleep(2)

            #     try:
            #         # カテゴリ選択するボタンを選択
            #         select_category_image: tuple = self.screen.image_locate(image_path="./images/select_category.png")
            #         pgui.click(select_category_image, duration=0.5)
            #         time.sleep(2)
            #     except Exception as e:
            #         self.logger.error(e)
            #         self.logger.error("カテゴリを選択できませんでした。処理を終了します。")
            #         break

            #     try:
            #         # デュエル・マスターズを選択
            #         select_duel_masters: tuple = self.screen.image_locate(image_path="./images/category_duel_masters.png")
            #         pgui.click(select_duel_masters, duration=0.5)
            #         time.sleep(2)
            #     except Exception as e:
            #         self.logger.error(e)
            #         self.logger.error("デュエル・マスターズを選択できませんでした。処理を終了します。")
            #         break

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
                break

            # 出品が完了しているか確認
            if self.screen.check_page(image_path="./images/syuppindekiteiruka.png") == False:
                self.logger.error("出品が完了していません。処理を終了します。")
                break

            self.web.page_back(count=8)
            self.logger.info("出品が完了したため、商品ページに戻ります。")
            time.sleep(2)

            if self.screen.check_page(image_path="./images/mercari_copy.png") == False:
                self.logger.error("商品ページに戻ることが出来ていません。処理を終了します。")
                break

            try:
                edit_item_button: tuple = self.screen.image_locate(image_path="./images/syouhinnnohensyuu.png")
                # 画像が取得できているか
                pgui.click(edit_item_button, duration=0.5)
                self.logger.info("商品の編集ボタンを押下")
                time.sleep(3)
            except Exception as e:
                self.logger.error(e)
                self.logger.error("商品の編集ボタンが選択できませんでした。処理を終了します。")
                break

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
                break

            try:
                # 削除するボタンを押下
                delete_popup_button: tuple = self.screen.image_locate(image_path="./images/sakujosuru.png")
                pgui.click(delete_popup_button, duration=0.5)
                time.sleep(2)
            except Exception as e:
                self.logger.error(e)
                self.logger.error("削除するボタンが選択できませんでした。処理を終了します。")
                break

            pgui.hotkey("ctrl", "w")
        self.logger.info("自動再出品を終了します")
        self.logger.info("----------------end----------------")
        pgui.alert(text="自動再出品を終了します", title="終了通知", button="OK")
