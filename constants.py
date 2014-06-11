import os

from compat import is_win32, is_py2, unicode_filename

DEFAULT_PLAYER_ARGUMENTS = "{filename}"

if is_win32:
    APPDATA = os.environ["APPDATA"]
    CONFIG_FILES = [os.path.join(APPDATA, "livestreamer", "livestreamerrc")]
    PLUGINS_DIR = os.path.join(APPDATA, "livestreamer", "plugins")
else:
    XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", "~/.config")
    CONFIG_FILES = [
        os.path.expanduser(XDG_CONFIG_HOME + "/livestreamer/config"),
        os.path.expanduser("~/.livestreamerrc")
    ]
    PLUGINS_DIR = os.path.expanduser(XDG_CONFIG_HOME + "/livestreamer/plugins")

# Turn the paths into unicode on Python 2 like they are on Python 3
if is_py2:
    PLUGINS_DIR = unicode_filename(PLUGINS_DIR)
    CONFIG_FILES = list(map(unicode_filename, CONFIG_FILES))


EXAMPLE_USAGE = """
example usage:

$ livestreamer twitch.tv/thegdstudio
Available streams: high, low, medium, mobile (worst), source (best)
$ livestreamer twitch.tv/thegdstudio high

Stream is now opened in player (default is VLC, if installed).

"""

STREAM_SYNONYMS = ["best", "worst"]
STREAM_PASSTHROUGH = ["hls", "http", "rtmp"]

__all__ = ["EXAMPLE_USAGE", "CONFIG_FILES", "PLUGINS_DIR",
           "STREAM_SYNONYMS", "STREAM_PASSTHROUGH", "DEFAULT_PLAYER_ARGUMENTS"]
