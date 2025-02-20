import spotipy

from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="app_cli_id",
    client_secret="app_cli_secret",
    redirect_uri="http://localhost:8888/callback",
    scope="user-read-currently-playing user-read-playback-state"
))

def get_current_track():
    current_track = sp.current_playback()
    if current_track and current_track["is_playing"]:
        track = current_track["item"]
        artist = track["artists"][0]["name"]
        title = track["name"]
        return f"{title} - {artist}"
    return "Nada tocando"

print(get_current_track())