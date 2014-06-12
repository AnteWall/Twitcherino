import os
from functools import partial
from PyQt4 import QtGui
from PyQt4 import Qt
from PyQt4 import QtWebKit

__author__ = 'Klante'


def clear_layout(layout):
    while layout.count() > 0:
        item = layout.takeAt(0)
        if not item:
            continue

        w = item.widget()
        if w:
            w.deleteLater()


def get_next_x_and_y_pos(x, y, add_x=2, break_on=8):
    x += add_x
    if x % break_on == 0:
        y += 4
        x = 0
    return x, y


def create_push_button(title, style=None, click=None):
    # Create Default Style
    if style is None:
        style = "QPushButton{background: #3b3b3b;color:#9b9b9b;}"

    btn = QtGui.QPushButton(title)
    btn.setStyleSheet(style)

    if click is not None:
        btn.clicked.connect(click)

    return btn


def create_label_image(image):
    pixmap = QtGui.QPixmap(os.getcwd() + image)
    image = QtGui.QLabel()
    image.setPixmap(pixmap)
    return image


def create_label(title, word_wrap=True, max_height=80, max_length=200):
    label = QtGui.QLabel(title)
    label.setMaximumWidth(max_length)
    label.setMaximumHeight(max_height)
    label.setWordWrap(word_wrap)
    return label


def create_web_image(image, width, height, template_image=False):
    web = QtWebKit.QWebView()
    web.setFixedHeight(height)
    web.setFixedWidth(width)
    if template_image:
        image = get_template_string(image, height, width)
    web.load(Qt.QUrl(image))
    return web


def get_template_string(string, height, width):
    string = string.replace("{width}", str(width))
    string = string.replace("{height}", str(height))
    return string


class TwitchGUIHelper(object):
    def __init__(self):
        self.main_content_layout = None
        self.menu_layout = None

    def get_main_content_layout(self):
        return self.main_content_layout

    def set_main_content_layout(self, layout):
        self.main_content_layout = layout

    def get_menu_layout(self):
        return self.menu_layout

    def create_streams_layout(self, streams, player):
        layout = QtGui.QGridLayout()
        x = y = 0

        for stream in streams:
            layout.addWidget(create_label(stream["channel"]["status"]), y, x, 1, 2)
            layout.addWidget(create_label("<b>" + stream["channel"]["name"] + "</b>"), y + 1, x, 1, 1)
            layout.addWidget(create_label("<b>" + str(stream["viewers"]) + "</b>"), y + 1, x + 1, 1, 1)
            layout.addWidget(
                create_web_image(stream["preview"]["template"], 200, 125, template_image=True),
                y + 2,
                x,
                1,
                2
            )
            play_func = partial(player.start_playing, stream["channel"]["url"])
            layout.addWidget(
                create_push_button("Watch", click=play_func),
                y + 3,
                x,
                1,
                2
            )

            x, y = get_next_x_and_y_pos(x, y)

        # If > 12 Streams, Fillout with empty Objects for positioning
        for i in range(len(streams), 12):
            layout.addWidget(self.stream_filler(220, 180), y, x, 3, 2)
            x, y = get_next_x_and_y_pos(x, y)

        return layout

    @staticmethod
    def create_games_list_layout(games, stream_func):
        layout = QtGui.QGridLayout()
        x = y = 0
        x = y = 0
        for game in games["top"]:
            layout.addWidget(
                create_label(game["game"]["name"], max_height=10, max_length=100),
                y,
                x
            )
            layout.addWidget(
                create_label("Viewers: "+str(game["viewers"]), max_height=20),
                y + 1,
                x
            )
            layout.addWidget(
                create_web_image(
                    game["game"]["box"]["template"], 100, 140, template_image=True),
                y + 2,
                x
            )
            view_game_func = partial(stream_func,game["game"]["name"])
            layout.addWidget(
                create_push_button("View Streams", click=view_game_func),
                y + 3,
                x
            )
            x, y = get_next_x_and_y_pos(x, y, add_x=1)

        return layout

    @staticmethod
    def stream_filler(width, height):
        filler = QtGui.QLabel()
        filler.setMinimumWidth(width)
        filler.setMinimumHeight(height)
        return filler

