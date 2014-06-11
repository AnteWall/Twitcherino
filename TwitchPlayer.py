__author__ = 'Klante'
from livestreamer import Livestreamer, NoPluginError, PluginError
from utils import find_default_player, stream_to_url, HTTPServer
from output import PlayerOutput
import os

class TwitchPlayer():
    def __init__(self):
        self.url = None
        self.player = None
        self.stream = None
        self.http = None
        self.play_url = None

    def start_playing(self, url):
        self.url = url
        print self.url
        self.get_streams()
        self.create_server()
        self.create_player()
        self.play()

    def get_streams(self):
        live = Livestreamer()
        print self.url
        live.set_option("http-ssl-verify", False)


        streams = None

        live.load_plugins(os.path.join(os.getcwd(), "plugins"))
        try:
            plugin = live.resolve_url(self.url)
            streams = plugin.get_streams()

            self.play_url = stream_to_url(streams.get("best"))
        except NoPluginError:
            print("No plugin can handle URL")
        except PluginError as err:
            print("{0}", err)

    def create_http_server(self):
        try:
            http = HTTPServer()
            http.bind()
        except:
            print("Failed to create HTTP server:")
        return http

    def create_server(self):
        self.http = self.create_http_server()

    def create_player(self):
        if self.play_url is not None:
            self.player = PlayerOutput(find_default_player(), filename=self.play_url)

    def play(self):
        if self.play_url is None:
            print("No Url to play so no player has been initiated")
        else:
            try:
                print ("Starting player...")
                self.player.open()
            except OSError as err:
                print ("Failed to Start Player {0}", err)

    def stop(self):
        print ("Closing player...")
        player.close()


"""
live = Livestreamer()
url = "http://twitch.tv/twitch"
streams = None

try:
    plugin = live.resolve_url(url)

    streams = plugin.get_streams()

    print streams

    stream = stream_to_url(streams.get("medium"))
    print stream
except NoPluginError:
    print("No plugin ca handle URL: {0}" ,url)
except PluginError as err:
    print("{0}" , err)

if not streams:
    print("No Streams Found")


#####################
# OPEN HTTP SERVER (VLC)
#####################


server = create_http_server()
player = PlayerOutput(find_default_player() ,filename=stream_to_url(streams.get("medium")))
   """
