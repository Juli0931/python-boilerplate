import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyClient:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.sp_oauth = SpotifyOAuth(client_id=self.client_id,
                                     client_secret=self.client_secret,
                                     redirect_uri=self.redirect_uri,
                                     scope='user-library-read user-read-private user-read-email')
        self.token_info = None

    def get_authorize_url(self):
        return self.sp_oauth.get_authorize_url()

    def get_access_token(self, code):
        self.token_info = self.sp_oauth.get_access_token(code)
        return self.token_info

    def create_spotify_instance(self, access_token):
        return spotipy.Spotify(auth=access_token)

    def get_access_token_from_cache(self):
        if not self.token_info:
            self.token_info = self.sp_oauth.get_cached_token()
        return self.token_info
