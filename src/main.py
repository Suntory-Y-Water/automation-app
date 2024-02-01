import PySimpleGUI as sg
import pyautogui as pgui
from scripts.auto_relist import AutoRelist
from scripts.auto_relist_sold_items import AutoRelistSoldItems


class GUI:
    def __init__(self):
        sg.theme("DarkGrey11")
        self.layout = self.create_layout()

    def create_layout(self):
        label_size = (12, 1)
        input_size = (20, 1)
        font_size = 14
        font_family_size = ("PlemolJP35 Console", font_size)

        layout = [
            [sg.Text("プログラムを選択してください\n", font=font_family_size)],
            [
                sg.Text("プログラム名:", font=font_family_size, size=label_size),
                sg.Combo(["自動再出品", "自動再出品(取引画面)"], default_value="自動再出品", key="program_name", font=font_family_size, size=input_size),
            ],
            [sg.Text("件数:", size=label_size, font=font_family_size), sg.InputText("", key="count", font=font_family_size, size=(10, 1))],
            [sg.Button("開始", font=font_family_size, bind_return_key=True)],
        ]
        return layout

    def start_selected_program(self, program_name, count):
        """GUIで選択されたプログラムを実行する。"""
        if program_name == "自動再出品":
            auto_relist = AutoRelist()
            auto_relist.run(count)

        if program_name == "自動再出品(取引画面)":
            auto_relist_sold_items = AutoRelistSoldItems()
            auto_relist_sold_items.run(count)

    def run_gui(self):
        window = sg.Window("メルカリ 作業自動化アプリ", self.layout)
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            if event == "開始":
                program_name = values["program_name"]
                count_str = values["count"]
                if count_str.isdigit():
                    is_value = pgui.confirm(f"{program_name}を開始しますか？", title="確認")
                    if is_value == "OK":
                        count = int(count_str)
                        self.start_selected_program(program_name, count)
                else:
                    pgui.alert("件数には数字を入力してください。", title="入力エラー")
        window.close()


if __name__ == "__main__":
    gui = GUI()
    gui.run_gui()
