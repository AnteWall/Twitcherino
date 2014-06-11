__author__ = 'Klante'
import requests
import os


class TwitchApi():
    def get_streams(self,limit=20):

        r = requests.get("https://api.twitch.tv/kraken/streams?limit="+str(limit))
        return r.json()

