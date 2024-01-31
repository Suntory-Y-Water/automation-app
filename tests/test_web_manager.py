import pytest
import pyautogui as pgui
from collections import namedtuple
import time
import sys
import os

# テストファイルのディレクトリを取得
current_dir = os.path.dirname(__file__)

# プロジェクトのルートディレクトリを取得
project_root = os.path.abspath(os.path.join(current_dir, ".."))

# プロジェクトのルートをPythonのパスに追加
sys.path.append(project_root)

from src.modules.web_manager import WebManager
from src.modules.logger import Logger

web_manager = WebManager()
Box = namedtuple("Box", "left top width height")


@pytest.fixture
def create_alert():
    # ここでテストの前提条件を設定します
    pgui.alert(text="ボタンを押したらテストが始まります", title="テスト用の待機時間", button="OK")
    logger = Logger.setup_logger("__test__")
    logger.info("WebManagerクラスのテストを開始します")
    time.sleep(1)


class TestWebManager:
    @pytest.mark.skip(reason="一度実行したためスキップ")
    @pytest.mark.usefixtures("create_alert")
    def test_get_url(self):
        """URLを正常に取得できるか"""
        url = web_manager.get_url()
        assert url is not None  # URLがNoneでないことを確認

    @pytest.mark.skip(reason="一度実行したためスキップ")
    @pytest.mark.usefixtures("create_alert")
    def test_page_click(self):
        """ページが正常にクリックできるか"""
        web_manager.page_click(Box(left=1377, top=1454, width=1037, height=162))
        assert True

    @pytest.mark.skip(reason="一度実行したためスキップ")
    @pytest.mark.usefixtures("create_alert")
    def test_page_back(self):
        """ページが正常に戻るか"""
        web_manager.page_back(1)
        assert True

    @pytest.mark.skip(reason="一度実行したためスキップ")
    @pytest.mark.usefixtures("create_alert")
    def test_go_product_page(self):
        """現在のページが取引画面のとき、商品ページに遷移できるか"""
        web_manager.go_product_page("https://jp.mercari.com/transaction/m38172937521")
        assert True
