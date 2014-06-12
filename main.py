__author__ = 'Klante'
import sys
from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui
from TwitchApi import TwitchApi
from TwitchPlayer import TwitchPlayer
from TwitchGui.TwitchGuiHelper import TwitchGUIHelper, clear_layout, create_push_button, create_label_image


class GUI(QtGui.QDialog):
    def __init__(self):
        super(GUI, self).__init__()
        self.helper = TwitchGUIHelper()
        self.layout = None
        self.main_content_box = None
        self.player = TwitchPlayer()
        self.twitch_api = TwitchApi()
        # Init Functions
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Twitcherino")
        self.setStyleSheet("QDialog{background-color:#1f1f1f;}")

        self.layout = QtGui.QHBoxLayout()

        self.main_content_box = self.create_main_wrapper()

        self.layout.addWidget(self.create_menu_box())
        self.layout.addWidget(self.main_content_box, alignment=QtCore.Qt.AlignRight)

        self.setLayout(self.layout)
        self.show()

    def create_menu_box(self):
        hbox = QtGui.QGroupBox()
        hbox.setMinimumWidth(200)
        hbox.setMaximumWidth(200)

        h_layout = QtGui.QVBoxLayout()
        hbox.setStyleSheet("QGroupBox{ border:none;color:#9b9b9b;}")

        logo = create_label_image("/img/logo.png")
        h_layout.addWidget(logo, alignment=QtCore.Qt.AlignCenter)

        top_streams_btn = create_push_button("Channels", click=lambda: self.show_channels())
        h_layout.addWidget(top_streams_btn)

        game_list_btn = create_push_button("Games", click=lambda: self.show_games_list())
        h_layout.addWidget(game_list_btn)

        btn_close = create_push_button("Exit", click=Qt.QApplication.instance().quit)
        h_layout.addWidget(btn_close, alignment=QtCore.Qt.AlignBottom)

        hbox.setLayout(h_layout)
        return hbox

    def show_channels(self):
        clear_layout(self.helper.get_main_content_layout())
        QtCore.QObjectCleanupHandler().add(self.helper.get_main_content_layout())
        streams = self.twitch_api.get_streams(limit=12)
        self.helper.set_main_content_layout(self.helper.create_streams_layout(streams["streams"], self.player))
        self.main_content_box.setLayout(self.helper.get_main_content_layout())

    def show_streams_by_game(self, game):
        clear_layout(self.helper.get_main_content_layout())
        QtCore.QObjectCleanupHandler().add(self.helper.get_main_content_layout())
        streams = self.twitch_api.get_game_streams(game, limit=12)
        self.helper.set_main_content_layout(self.helper.create_streams_layout(streams["streams"], self.player))
        self.main_content_box.setLayout(self.helper.get_main_content_layout())

    def show_games_list(self):
        clear_layout(self.helper.get_main_content_layout())
        QtCore.QObjectCleanupHandler().add(self.helper.get_main_content_layout())
        games = self.twitch_api.get_games(limit=24)
        self.helper.set_main_content_layout(self.helper.create_games_list_layout(games, self.show_streams_by_game))
        self.main_content_box.setLayout(self.helper.get_main_content_layout())

    def create_main_wrapper(self):
        grid_box = QtGui.QGroupBox()
        grid_box.setStyleSheet("QGroupBox{border:none;color:#9b9b9b;background:#f9f9f9;}")
        streams = self.twitch_api.get_streams(limit=12)
        self.helper.set_main_content_layout(self.helper.create_streams_layout(streams["streams"], self.player))
        grid_box.setLayout(self.helper.get_main_content_layout())
        return grid_box


def main():
    app = Qt.QApplication(sys.argv)
    g = GUI()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


