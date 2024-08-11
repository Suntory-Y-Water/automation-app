from .base_script import BaseScript
import pyautogui as pgui
import time


class AutoRelist(BaseScript):
    """自動再出品(売れていない商品)"""

    def __init__(self):
        super().__init__()
        self.logger.info("自動再出品を開始します")

    def run(self, count=1):
        self.logger.info("---------------start---------------")
        for _ in range(count):
            current_url = self.web.get_url()
            self.logger.info(f"この商品を再出品します商品URL: {current_url}")

            # 画像あり再出品を押下する
            self.logger.info("画像あり再出品を押下します")
            is_relist = self.click_and_wait(image_path="./images/mercari_copy.png")
            if is_relist is False:
                self.logger.error("画像あり再出品を押下できませんでした、処理を終了します")
                break
            
            # 商品ページで出品するを押下する
            is_relist_button_clicked = self.scroll_to_bottom_and_click(image_path="./images/syuppinnsuru.png")
            if is_relist_button_clicked is False:
                break
            
            # 出品するボタンを押下したあと、出品が完了できているか確認する
            is_fix_relist = self.check_relist()
            if is_fix_relist is False:
                break

            self.web.page_back(count=8)
            self.logger.info("出品が完了したため、商品ページに戻ります")
            time.sleep(2)

            if self.screen.image_locate(image_path="./images/mercari_copy.png") == None:
                self.logger.error("商品ページに戻ることが出来ていません処理を終了します")
                break

            # 商品の編集ページで通常のボタンかタイムセールのボタンかを判定
            # edit_pageやedit_time_sale_pageはタプル型またはNoneで返ってくる
            edit_page = self.screen.image_locate(image_path="./images/syouhinnnohensyuu.png")
            edit_time_sale_page = self.screen.image_locate(image_path="./images/time-sale-or-syouhinnohensyu.png")
            
            if edit_page:
                pgui.click(edit_page, duration=0.5)
                self.logger.info("通常の商品編集ボタンを押下しました")
            elif edit_time_sale_page:
                pgui.click(edit_time_sale_page, duration=0.5)
                self.logger.info("タイムセールの編集ボタンを押下しました")
            else:
                raise Exception("適編集ボタンが見つかりませんでした、処理を中止します")

            # 処理後の待機時間
            time.sleep(3)
            
            pgui.press("end")
            self.logger.info("商品の編集へ移動")
            time.sleep(2)

            self.logger.info("この商品を削除するボタンを押下します")
            is_delete_button = self.click_and_wait(image_path="./images/konosyouhinwosakujosuru.png", sleep_time=1)
            if is_delete_button is False:
                self.logger.error("この商品を削除するボタンが選択できませんでした処理を終了します")
                break

            self.logger.info("POPUPの削除するボタンを押下します")
            is_delete_popup_button = self.click_and_wait(image_path="./images/sakujosuru.png", sleep_time=2)
            if is_delete_popup_button is False:
                self.logger.error("削除するボタンが選択できませんでした処理を終了します")
                break


            pgui.hotkey("ctrl", "w")
        self.logger.info("自動再出品を終了します")
        self.logger.info("----------------end----------------")
        pgui.alert(text="自動再出品を終了します", title="終了通知", button="OK")
