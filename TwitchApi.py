__author__ = 'Klante'
import requests
import os


class TwitchApi():
    def get_streams(self,limit=20):
        r = requests.get("https://api.twitch.tv/kraken/streams?limit="+str(limit))
        return r.json()

    def get_games(self,limit=25):
        r = requests.get("https://api.twitch.tv/kraken/games/top?limit="+str(limit))
        return r.json()

    def get_game_streams(self,game,limit=20):
        r = requests.get("https://api.twitch.tv/kraken/streams/?game="+game+"&limit="+str(limit))
        return r.json()