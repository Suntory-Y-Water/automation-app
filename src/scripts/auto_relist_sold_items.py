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

    def run(self, count=1):
        self.logger.info("---------------start---------------")
        for _ in range(count):
            pgui.click(100, 100)
            current_url = self.web.get_url()
            self.logger.info(f"この商品を再出品します商品URL: {current_url}")
            pgui.click(100, 800)

            # 画像あり再出品を押下する
            is_relist = self.click_and_wait(image_path="./images/mercari_copy.png")
            if is_relist is False:
                # 超メルカリ祭で再出品ボタンが見えない場合、ページをスクロールする
                pgui.press('pagedown')
                time.sleep(0.3)
                # 再度クリックを試みる
                is_relist = self.click_and_wait(image_path="./images/mercari_copy.png")
                if is_relist is False:
                    break
            
            # 商品ページで出品するを押下する
            is_relist_button_clicked = self.scroll_to_bottom_and_click(image_path="./images/syuppinnsuru.png")
            if is_relist_button_clicked is False:
                break

            # 出品が完了しているか確認
            if self.screen.check_page(image_path="./images/syuppindekiteiruka.png") == False:
                self.logger.error(f"出品することが出来ませんでした。商品URL: {current_url} ")
                break

            pgui.hotkey("ctrl", "w")
            self.logger.info("出品が完了したため、次の商品を再出品します。")
        self.logger.info("売れた商品の自動再出品を終了します")
        self.logger.info("----------------end----------------")
        pgui.alert(text="売れた商品の自動再出品を終了します", title="終了通知", button="OK")
