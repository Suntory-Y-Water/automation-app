import os
import sys


class BaseScript:
    """実行ファイルが格納されているフォルダのベースクラス"""

    def __init__(self):
        self.setup_path()

    def setup_path(self):
        """スクリプトごとにモジュールパスを設定する"""
        current_dir = os.path.dirname(__file__)
        src_dir = os.path.abspath(os.path.join(current_dir, ".."))
        if src_dir not in sys.path:
            sys.path.append(src_dir)
