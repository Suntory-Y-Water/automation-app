import pytest
import time
import pyautogui as pgui
import sys
import os

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from src.modules.screen import ScreenManagement
from src.modules.logger import Logger

# ScreenManagementクラスのインスタンスを作成
screen_manager = ScreenManagement()


@pytest.fixture
def create_alert():
    # ここでテストの前提条件を設定します
    pgui.alert(text="ボタンを押したらテストが始まります", title="テスト用の待機時間", button="OK")
    logger = Logger.setup_logger("__test__")
    logger.info("テストを開始します")

    time.sleep(1)


# 画像認識のテストケースを含むテストクラス
class TestScreenManagement:
    @pytest.mark.skip(reason="一度実行したためスキップ")
    @pytest.mark.usefixtures("create_alert")
    def test_reloading_page(self):
        """画像が読み込めなかったとき正常にリロードするか"""
        result = screen_manager.reloading_page(None, wait_time=0)
        assert result is None

    @pytest.mark.skip(reason="一度実行したためスキップ")
    @pytest.mark.usefixtures("create_alert")
    def test_image_locate(self):
        # 画像を認識して座標を取得
        result = screen_manager.image_locate("./images/syuppinnsuru.png")
        print(result)
        assert result is not None

    # 存在しない画像をエラー吐くかのテスト
    @pytest.mark.skip(reason="一度実行したためスキップ")
    @pytest.mark.usefixtures("create_alert")
    def test_image_locate(self):
        with pytest.raises(pgui.ImageNotFoundException):
            # 画像が存在しない場合、pgui.ImageNotFoundException が発生することを確認
            screen_manager.image_locate("./images/syuppinnsyouhinwomiru.png")

    # ページの存在確認のテスト
    @pytest.mark.skip(reason="一度実行したためスキップ")
    @pytest.mark.usefixtures("create_alert")
    def test_check_page(self):
        # 画像が画面上に存在するか確認
        # 商品の編集をするページが存在するか確認
        result = screen_manager.check_page("./images/syouhinnnohensyuu.png")
        assert result is True

    # ページの存在確認のテスト
    @pytest.mark.skip(reason="一度実行したためスキップ")
    @pytest.mark.usefixtures("create_alert")
    def test_time_sale_check_page(self):
        # タイムセールページが存在するか確認
        result = screen_manager.check_page("./images/time-sale-or-syouhinnohensyu.png")
        assert result is True

    # ページの存在確認のテスト
    @pytest.mark.usefixtures("create_alert")
    def test_price_ok_check_page(self):
        # タイムセールページが存在するか確認
        result = screen_manager.check_page("./images/time-sale-or-syouhinnohensyu.png")
        assert result is True
