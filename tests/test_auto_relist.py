import pytest
import time
import pyautogui as pgui
import sys
import os

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from src.modules.logger import Logger
from src.modules.screen import ScreenManagement
from src.modules.web_manager import WebManager

screen = ScreenManagement()
web = WebManager()
logger = Logger.setup_logger("__test__")


@pytest.fixture
def create_alert():
    # ここでテストの前提条件を設定します
    pgui.alert(text="ボタンを押したらテストが始まります", title="テスト用の待機時間", button="OK")
    logger.info("テストを開始します")

    time.sleep(1)


class TestIntegrationAutoRelist:
    """結合テスト用のテストケース"""

    @pytest.mark.skip(reason="一度実行したためスキップ")
    @pytest.mark.usefixtures("create_alert")
    def test_relist_and_check_page(self):
        """再出品を実行して、画面の一番下までスクロールし、出品できているか確認する"""

        current_url = web.get_url()
        logger.info(f"出品する商品は{current_url}です。")

        mercari_copy_image: tuple = screen.image_locate(image_path="./images/mercari_copy.png")
        # 画像が取得できているか
        assert mercari_copy_image is not None
        pgui.click(mercari_copy_image, duration=0.5)
        logger.info("画像あり再出品を選択")
        time.sleep(10)

        if screen.check_page(image_path="./images/category_hobby_page.png") == True:
            web.page_back(count=5)
            logger.info("カテゴリページでフリーズしたため、商品ページに戻ります。")
            time.sleep(2)

            # 画像あり再出品ボタンとかぶらなくさせる処置
            pgui.moveTo(100, 100)
            if screen.check_page(image_path="./images/mercari_copy.png") == False:
                logger.info("商品ページに戻ることが出来ていません。")
                web.page_back(count=1)
                time.sleep(1)

            # 商品ページから再出品を実行するため、次へキーで編集ページへ移動
            pgui.hotkey("alt", "right")
            time.sleep(2)

            # カテゴリ選択するボタンが読み込めるか確認
            select_category_image: tuple = screen.image_locate(image_path="./images/select_category.png")
            pgui.click(select_category_image, duration=0.5)
            time.sleep(2)
            assert select_category_image is not None

            # デュエル・マスターズを選択できるか確認
            select_duel_masters: tuple = screen.image_locate(image_path="./images/category_duel_masters.png")
            pgui.click(select_duel_masters, duration=0.5)
            time.sleep(2)
            assert select_duel_masters is not None

        # 出品するボタンを押すために画面一番下へスクロール
        pgui.press("end")
        time.sleep(2)

        relist_image: tuple = screen.image_locate(image_path="./images/syuppinnsuru.png")
        pgui.click(relist_image, duration=0.5)
        assert relist_image is not None
        logger.info("出品するボタンを押下")
        time.sleep(2)

        check_relist_image = screen.check_page(image_path="./images/syuppindekiteiruka.png")
        assert check_relist_image is True

    @pytest.mark.skip(reason="一度実行したためスキップ")
    @pytest.mark.usefixtures("create_alert")
    def test_page_back(self):
        """
        結合テストの橋渡し用のテストケース
        商品出品後に正しく商品ページに戻れているか確認する
        """
        web.page_back(count=4)
        logger.info("ページバックを実行")
        time.sleep(2)

        check_page_back_image = screen.check_page(image_path="./images/mercari_copy.png")
        assert check_page_back_image is True

    @pytest.mark.skip(reason="一度実行したためスキップ")
    @pytest.mark.usefixtures("create_alert")
    def test_edit_and_delete_item(self):
        """商品を編集して削除する"""
        edit_item_button: tuple = screen.image_locate(image_path="./images/syouhinnnohensyuu.png")
        # 画像が取得できているか
        assert edit_item_button is not None
        pgui.click(edit_item_button, duration=0.5)
        logger.info("商品の編集ボタンを押下")
        time.sleep(3)

        pgui.press("end")
        logger.info("商品の編集へ移動")
        time.sleep(2)

        # この商品を削除するボタンを押下
        delete_button: tuple = screen.image_locate(image_path="./images/konosyouhinwosakujosuru.png")
        assert delete_button is not None
        pgui.click(delete_button, duration=0.5)
        time.sleep(1)

        # この商品を削除するボタンを押下
        delete_popup_button: tuple = screen.image_locate(image_path="./images/sakujosuru.png")
        assert delete_popup_button is not None
        pgui.click(delete_popup_button, duration=0.5)
        time.sleep(2)

        pgui.hotkey("ctrl", "w")
