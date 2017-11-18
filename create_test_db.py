from models import Track, TrackFollow, User, UserFollow

from gwa_spotify_api import SpotifyAuthAPI

api = SpotifyAuthAPI()

print(api.get('me'))
