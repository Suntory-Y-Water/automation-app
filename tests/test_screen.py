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
    logger.info(f"{__name__}のテストを開始します")

    time.sleep(1)


# 画像認識のテストケースを含むテストクラス
class TestScreenManagement:
    @pytest.mark.skip(reason="2024/08/11")
    @pytest.mark.usefixtures("create_alert")
    def test_image_locate(self):
        # 画像を認識して座標を取得する
        result = screen_manager.image_locate("./images/mercari_copy.png")
        assert result is not None

        # 画像が存在しない場合はNoneを返す
        result2 = screen_manager.image_locate("./images/syuppindekiteiruka.png")
        assert result2 is None