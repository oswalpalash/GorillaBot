from plugins.util import command
import requests, re

SPOTIFY_URI_REGEX = r"(?<=spotify:)(?:track|album|artist):[a-zA-Z0-9]{22}"
ENDPOINT = "https://api.spotify.com/v1/%ss/%s"

@command()
def spotify(m):
    spotify_uris = re.findall(SPOTIFY_URI_REGEX, m.body)
    for spotify_uri in spotify_uris:
        try:
            type, id = _parse_spotify_uri(spotify_uri)
            r = requests.get(ENDPOINT % (type, id))
            if r.status_code != 200:
                continue
            response = r.json()
            if type == "track" or type == "album":
                m.bot.private_message(m.location, ' - '.join([response["artists"][0]["name"], response["name"]]))
            else:
                m.bot.private_message(m.location, response["name"])
        except ValueError:
            m.bot.logger.error("Invalid Spotify URI: %s" % spotify_uri)
            pass

def _parse_spotify_uri(s):
    [type, id] = s.split(':')
    return type, id
