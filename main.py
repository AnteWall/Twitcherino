from PyQt4 import Qt


__author__ = 'Klante'

from TwitchApi import TwitchApi
import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import QWebView

import urllib
from TwitchPlayer import TwitchPlayer
from functools import partial


class GUI(QDialog):
    def __init__(self, streams):
        super(GUI, self).__init__()
        self.main_wrapper_layout = None
        self.menu_bar_layout = None
        self.main_wrapper_box = None
        self.player = TwitchPlayer()
        self.twitch_api = TwitchApi()
        # Init Functions
        self.init_ui(streams)


    def init_ui(self, streams):
        self.setWindowTitle("Twitcherino")

        self.setStyleSheet("QDialog{background-color:#1f1f1f;}")
        main_layout = QHBoxLayout()
        self.main_wrapper_box = self.create_main_wrapper(streams)
        main_layout.addWidget(self.create_menu_bar())
        main_layout.addWidget(self.main_wrapper_box, alignment=Qt.AlignRight)
        self.setLayout(main_layout)
        self.resize(720, 480)
        self.show()


    def create_menu_bar(self):
        hbox = QGroupBox()
        hbox.setMinimumWidth(200)
        hbox.setMaximumWidth(200)
        h_layout = QVBoxLayout()
        hbox.setStyleSheet("QGroupBox{ border:none;color:#9b9b9b;}")

        # ###################
        # Logo        #
        # ###################
        pix = QPixmap(os.getcwd() + "/img/logo.png")
        logo = QLabel()
        logo.setPixmap(pix)
        h_layout.addWidget(logo, alignment=Qt.AlignCenter)

        # Game List Button
        game_btn = QPushButton("Games")
        game_btn.setStyleSheet("QPushButton{background: #3b3b3b;color:#9b9b9b;}")
        h_layout.addWidget(game_btn)
        game_btn.clicked.connect(lambda: self.create_games_list())

        # ###################
        # Exit Button    #
        # ###################
        btn_close = QPushButton("Exit")
        btn_close.setStyleSheet("QPushButton{background: #3b3b3b;color:#9b9b9b;}")
        h_layout.addWidget(btn_close, alignment=Qt.AlignBottom)
        btn_close.clicked.connect(QApplication.instance().quit)

        self.menu_bar_layout = h_layout
        hbox.setLayout(h_layout)
        return hbox

    def create_gamelist_layout(self, games):
        game_list_layout = QGridLayout()
        x = y = 0
        for game in games["top"]:
            game_list_layout.addWidget(self.create_stream_title(game["game"]["name"], max_height=10, max_length=100), y,
                                       x)
            game_list_layout.addWidget(self.create_views_count(game["viewers"], max_height=20), y + 1, x)
            game_list_layout.addWidget(self.create_channel_image(game["game"]["box"]["template"], 100, 140), y + 2, x)
            game_list_layout.addWidget(self.create_get_game_streams_btn(game["game"]["name"]), y + 3, x)

            # Calculate Row and Coulmn
            x += 1
            if x % 8 == 0:
                y += 4
                x = 0
        return game_list_layout

    def create_get_game_streams_btn(self,game):
        """
        Creates a button that will launch a Stream based on url
        @param url: url string
        @return: QButton
        """
        watch_btn = QPushButton("View Streams")
        watch_btn.setStyleSheet("QPushButton{background: #3b3b3b;color:#9b9b9b;}")
        watch_btn.clicked.connect(partial(self.create_request_game_streams, game))
        return watch_btn

    def create_request_game_streams(self,game):
        self.clear_layout(self.main_wrapper_layout)
        streams = self.twitch_api.get_game_streams(game,limit=12)
        QObjectCleanupHandler().add(self.main_wrapper_layout)
        self.main_wrapper_layout = self.create_streams_layout(streams)
        self.main_wrapper_box.setLayout(self.main_wrapper_layout)

    def create_games_list(self):
        self.clear_layout(self.main_wrapper_layout)
        QObjectCleanupHandler().add(self.main_wrapper_layout)
        self.main_wrapper_layout = self.create_gamelist_layout(self.twitch_api.get_games(limit=24))
        self.main_wrapper_box.setLayout(self.main_wrapper_layout)

    def clear_layout(self, layout):
        while layout.count() > 0:
            item = layout.takeAt(0)
            if not item:
                continue

            w = item.widget()
            if w:
                w.deleteLater()


    def create_stream_title(self, status, max_height=80, max_length=320):
        title_lbl = QLabel(status)
        title_lbl.setMaximumWidth(max_length)
        title_lbl.setMaximumHeight(max_height)
        title_lbl.setWordWrap(True)
        return title_lbl

    def create_channel_name(self, name):
        channel_lbl = QLabel()
        channel_lbl.setWordWrap(True)
        channel_lbl.setMaximumWidth(320)
        channel_lbl.setText("<b>" + name + "</b>")
        return channel_lbl

    def create_channel_image(self, url, w, h):
        web = QWebView()
        width = w
        height = h
        web.setFixedHeight(height)
        web.setFixedWidth(width)
        string = url
        string = string.replace("{width}", str(width))
        string = string.replace("{height}", str(height))
        web.load(QUrl(string))
        return web

    def create_watch_btn(self, url):
        """
        Creates a button that will launch a Stream based on url
        @param url: url string
        @return: QButton
        """
        watch_btn = QPushButton("Watch")
        watch_btn.setStyleSheet("QPushButton{background: #3b3b3b;color:#9b9b9b;}")
        watch_btn.clicked.connect(partial(self.player.start_playing, url))
        return watch_btn

    def create_views_count(self, views, max_height=40):
        views_lbl = QLabel("<b>Viewers: </b>" + str(views))
        views_lbl.setMaximumHeight(max_height)
        return views_lbl

    def create_streams_layout(self,streams):
        grid_layout = QGridLayout()

        x = y = 0
        for s in streams["streams"]:
            grid_layout.addWidget(self.create_stream_title(s["channel"]["status"]), y, x, 1, 2)
            grid_layout.addWidget(self.create_channel_name(s["channel"]["name"]), y + 1, x)
            grid_layout.addWidget(self.create_views_count(s["viewers"]), y + 1, x + 1, alignment=Qt.AlignRight)
            grid_layout.addWidget(self.create_channel_image(s["preview"]["template"], 200, 125), y + 2, x, 1, 2)
            grid_layout.addWidget(self.create_watch_btn(s["channel"]["url"]), y + 3, x, 1, 2)

            # Calculate Row and Coulmn
            x += 2
            if x % 8 == 0:
                y += 4
                x = 0

        self.main_wrapper_layout = grid_layout
        return grid_layout

    def create_main_wrapper(self, streams):
        grid_box = QGroupBox()
        grid_box.setStyleSheet("QGroupBox{border:none;color:#9b9b9b;background:#f9f9f9;}")

        grid_layout = self.create_streams_layout(streams)
        grid_box.setLayout(grid_layout)
        return grid_box

    def load_image(self, url):
        return urllib.urlopen(url).read()

    def download_image(self, url):
        manager = QNetworkAccessManager()
        request = QNetworkRequest(url)
        manager.finished.connect(self.download_finished)
        reply = manager.get(request)

    def download_finished(self):
        print "Finished"


def main():
    app = QApplication(sys.argv)
    twitch = TwitchApi()
    s = twitch.get_streams(limit=12)
    gui = GUI(s)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


