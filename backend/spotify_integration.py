# import spotipy
# from spotipy.oauth2 import SpotifyOAuth

# class SpotifyClient:
#     def __init__(self, client_id, client_secret, redirect_uri):
#         self.client_id = client_id
#         self.client_secret = client_secret
#         self.redirect_uri = redirect_uri
#         self.sp_oauth = SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, scope='user-library-read')

#     def get_authorize_url(self):
#         return self.sp_oauth.get_authorize_url()

#     def get_access_token(self, code):
#         token_info = self.sp_oauth.get_access_token(code)
#         return token_info['access_token']

#     def create_spotify_instance(self, access_token):
#         return spotipy.Spotify(auth=access_token)

import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyClient:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorize_url(self):
        sp_oauth = SpotifyOAuth(client_id=self.client_id,
                                client_secret=self.client_secret,
                                redirect_uri=self.redirect_uri,
                                scope="user-library-read user-read-private user-read-email")
        auth_url = sp_oauth.get_authorize_url()
        return auth_url

    def get_access_token(self, code):
        sp_oauth = SpotifyOAuth(client_id=self.client_id,
                                client_secret=self.client_secret,
                                redirect_uri=self.redirect_uri,
                                scope="user-library-read user-read-private user-read-email")
        token_info = sp_oauth.get_access_token(code)
        return token_info['access_token']

    def create_spotify_instance(self, access_token):
        sp = spotipy.Spotify(auth=access_token)
        return sp

    def get_audio_features(self, sp, track_ids):
        audio_features = sp.audio_features(tracks=track_ids)
        return audio_features
