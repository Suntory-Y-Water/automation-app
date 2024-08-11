from .base_script import BaseScript
import pyautogui as pgui


class AutoRelistSoldItems(BaseScript):
    """自動再出品(売れた商品)"""

    def __init__(self):
        super().__init__()
        self.logger.info("売れた商品の自動再出品を開始します")

    def run(self, count=1):
        self.logger.info("---------------start---------------")
        for _ in range(count):
            current_url = self.web.get_url()
            self.web.go_product_page(current_url)
            self.logger.info(f"この商品を再出品します商品URL: {current_url}")

            # 画像あり再出品を押下する
            is_relist = self.click_and_wait(image_path="./images/mercari_copy.png")
            if is_relist is False:
                break
            
            # 商品ページで出品するを押下する
            is_relist_button_clicked = self.scroll_to_bottom_and_click(image_path="./images/syuppinnsuru.png")
            if is_relist_button_clicked is False:
                break
            
            # 出品するボタンを押下したあと、出品が完了できているか確認する
            is_fix_relist = self.check_relist()
            if is_fix_relist is False:
                break

            pgui.hotkey("ctrl", "w")
            self.logger.info("出品が完了したため、次の商品を再出品します")
        self.logger.info("売れた商品の自動再出品を終了します")
        self.logger.info("----------------end----------------")
        pgui.alert(text="売れた商品の自動再出品を終了します", title="終了通知", button="OK")
