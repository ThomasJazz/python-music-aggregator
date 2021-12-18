import spotipy as spy
import spotipy.oauth2
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyHelper():
    def __init__(self, client_id, client_secret, username=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.redirect_uri = 'http://localhost:8080/'
        #self.token = self.__get_token()
        oauth = self.__get_username_oauth(username)

        self.client = spy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

        
        #self.credentials = spy.oauth2.SpotifyClientCredentials()

    ########################################
    # ------------------------------------ #
    # --------- Public Functions --------- #
    # ------------------------------------ #
    ########################################

    # Returns the discography of an artist
    def get_artist_albums(self, artist_id):
        # Build request URI
        artist_uri = f'spotify:artist:{artist_id}'

        results = self.client.artist_albums(artist_uri, album_type='album')

        albums = results['items']
        while results['next']:
            results = spotify.next(results)
            albums.extend(results['items'])

        return albums
    

    def get_artist_albums_summary(self, artist_id):
        album_info = self.get_artist_albums(artist_id)
        summary = []

        for album in album_info:
            name = album['name']
            release_date = album['release_date']
            total_tracks = album['total_tracks']
            artists_in_album = []

            for artist in album['artists']:
                artists_in_album.append(artist['name'])
            
            album_dict = {'name': name, 'release_date': release_date, 'total_tracks': total_tracks, 'artists_in_album': artists_in_album}
            summary.append(album_dict)
        
        return summary

    def get_artist(self, artist_uri):
        return self.client.artist(artist_uri)

    
    def get_user_playlists(self, username):
        playlists = self.client.user_playlists(username)

        return playlists
    
    def get_user(self, username):
        return self.client.user(username)

    
    def get_current_user(self, username):
        return self.client.current_user()

    
    def get_recently_played(self, username:str, limit:50):
        client = self.__get_client_with_scope('user-read-recently-played')

        return client.current_user_recently_played(limit=limit)
    

    def get_user_recently_played_artists(self, username:str, limit: 50):
        recent_artists = []
        
        recent_songs = self.get_recently_played(username, limit)

        # Loop through all the recent tracks
        for song in recent_songs['items']:
            # Loop through all the artists associated with a track
            for artist in song['track']['artists']:
                artist_id = artist['id']
                artist_uri = f'spotify:artist:{artist_id}'
                artist_details = self.get_artist(artist_uri)
                artist_genres = artist_details['genres']
                artist_name = artist['name']

                # Append dictionary to output list
                recent_artists.append({
                    'name': artist_name,
                    'id': artist_id,
                    'uri': artist_uri,
                    'genres': artist_genres
                })
        
        return recent_artists
    
    
    def get_user_top_artists(self, username, limit=20, time_range='long_term'):
        client = self.__get_client_with_scope('user-top-read')
        return client.current_user_top_artists(limit=limit, time_range=time_range)

    def get_user_top_artists_summary(self, username, limit=20, time_range='long_term'):
        """Returns a summarized list of the users top artists over a given time range

        Args:
            username (str): The username to pull top artists for
            limit (int, optional): The number of top artists to pull. Defaults to maximum of 20.
            time_range (str, optional): 'short_term'(~4 weeks), 'medium_term' (~6 months), or 'long_term' (all time). Defaults to 'long_term'

        Returns:
            (list): List of dictionaries containing top artist info
        """

        artist_details = self.get_user_top_artists(username, limit, time_range)
        return self.get_artists_summary(artist_details)
    
    def get_artists_summary(self, artist_details:list):
        artists = []
        for artist in artist_details['items']:
            artist_id = artist['id']
            artist_uri = f'spotify:artist:{artist_id}'
            artist_details = self.get_artist(artist_uri)
            artist_genres = artist_details['genres']
            artist_name = artist['name']

            artists.append({
                'name': artist_name,
                #'id': artist_id,
                #'uri': artist_uri,
                'genres': artist_genres
            })
        
        return artists
    
    def get_artist_names_from_summary(self, artist_summary:list):
        names = []
        for artist in artist_summary:
            names.append(artist['name'])

        return names


    ########################################
    # ------------------------------------ #
    # -------- Private Functions --------- #
    # ------------------------------------ #
    ########################################
    def __get_username_oauth(self, username):
        oauth = spy.oauth2.SpotifyOAuth(self.client_id, 
            self.client_secret, 
            redirect_uri=self.redirect_uri, 
            scope='playlist-read-private', 
            username=username)

        return oauth

    def __get_token(self):
        return self.__get_credentials().get_access_token()
        
    def __get_credentials(self):
        return SpotifyClientCredentials(self.client_id, self.client_secret)

    def __get_base_client(self):
        pass

    def __get_client_with_scope(self, scope:str):
        client = spy.Spotify(auth_manager=spy.oauth2.SpotifyOAuth(client_id=self.client_id, 
            client_secret=self.client_secret, 
            scope=scope,
            redirect_uri=self.redirect_uri))
        
        return client
        
    def __get_oauth_client(self):
        pass