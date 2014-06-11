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
        self.player = TwitchPlayer()
        self.init_ui(streams)

    def init_ui(self, streams):
        self.setWindowTitle("Twitcherino")

        self.setStyleSheet("QDialog{background-color:#1f1f1f;}")
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.create_menu_bar())
        main_layout.addWidget(self.create_stream_layout(streams), alignment=Qt.AlignRight)
        self.setLayout(main_layout)
        self.resize(720, 480)
        self.show()

    def create_menu_bar(self):
        hbox = QGroupBox()
        hbox.setMinimumWidth(200)
        h_layout = QVBoxLayout()

        hbox.setStyleSheet("QGroupBox{ border:none;color:#9b9b9b;}")

        # ###################
        # Logo        #
        # ###################
        pix = QPixmap(os.getcwd() + "/img/logo.png")
        logo = QLabel()
        logo.setPixmap(pix)
        h_layout.addWidget(logo, alignment=Qt.AlignCenter)

        # ###################
        # Exit Button    #
        # ###################
        btn_close = QPushButton("Exit")
        btn_close.setStyleSheet("QPushButton{background: #3b3b3b;color:#9b9b9b;}")
        h_layout.addWidget(btn_close, alignment=Qt.AlignBottom)
        btn_close.clicked.connect(QApplication.instance().quit)

        hbox.setLayout(h_layout)
        return hbox

    def create_stream_title(self, status):
        title_lbl = QLabel(status)
        title_lbl.setMaximumWidth(320)
        title_lbl.setWordWrap(True)
        return title_lbl

    def create_channel_name(self, name):
        channel_lbl = QLabel()
        channel_lbl.setWordWrap(True)
        channel_lbl.setMaximumWidth(320)
        channel_lbl.setText("<b>" + name + "</b>")
        return channel_lbl

    def create_channel_image(self, url):
        web = QWebView()
        width = 200
        height = 125
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

    def create_views_count(self, views):
        views_lbl = QLabel("<b>Viewers: </b>"+str(views))
        return views_lbl

    def create_stream_layout(self, streams):
        grid_box = QGroupBox("Streams")
        grid_layout = QGridLayout()
        grid_box.setStyleSheet("QGroupBox{border:none;color:#9b9b9b;background:#f9f9f9;}")

        x = y = 0
        for s in streams["streams"]:
            grid_layout.addWidget(self.create_stream_title(s["channel"]["status"]), y, x, 1, 2)
            grid_layout.addWidget(self.create_channel_name(s["channel"]["name"]), y + 1, x)
            grid_layout.addWidget(self.create_views_count(s["viewers"]), y + 1, x + 1, alignment=Qt.AlignRight)
            grid_layout.addWidget(self.create_channel_image(s["preview"]["template"]), y + 2, x, 1, 2)
            grid_layout.addWidget(self.create_watch_btn(s["channel"]["url"]), y + 3, x, 1, 2)


            # Calculate Row and Coulmn
            x += 2
            if x % 8 == 0:
                y += 4
                x = 0
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


